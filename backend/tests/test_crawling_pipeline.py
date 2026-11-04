"""
Automated Unit and Integration Tests for Autonomous Web Scraping & Crawling Engine.
Tests Scrapy, Crawl4AI, Trafilatura adapters, Deduplication, Provenance, and API endpoints.
"""

import pytest
from app.integrations.web_crawling.deduplication import deduplication_engine
from app.integrations.web_crawling.source_provenance import provenance_tracker
from app.integrations.web_crawling.trafilatura_adapter import trafilatura_adapter
from app.integrations.web_crawling.crawl4ai_adapter import crawl4ai_adapter
from app.integrations.web_crawling.content_extractor import content_extractor
from app.integrations.web_crawling.scrapy_adapter import DomainRateLimiter
from app.integrations.web_crawling.crawl_manager import crawl_manager


@pytest.fixture(autouse=True)
def clean_state():
    deduplication_engine.clear()


def test_canonical_url_normalization():
    """Verify canonical URL normalization strips tracking params, fragments, and standard ports."""
    url1 = "https://arxiv.org:443/abs/2304.12345?utm_source=twitter&utm_medium=social#abstract"
    url2 = "https://arxiv.org/abs/2304.12345"

    norm1 = deduplication_engine.normalize_url(url1)
    norm2 = deduplication_engine.normalize_url(url2)

    assert norm1 == norm2
    assert "utm_source" not in norm1
    assert "#abstract" not in norm1
    assert ":443" not in norm1


def test_url_and_content_deduplication():
    """Verify duplicate URLs and identical body texts are correctly detected and flagged."""
    sample_text = (
        "We propose a novel Siamese network for multitemporal change detection using Sentinel-1 SAR imagery. "
        "The architecture introduces dual-temporal spatial subtraction with cross-attention gating, achieving an "
        "F1-score of 94.2% on the SpaceNet dataset. Multiplicative speckle noise is effectively suppressed."
    )
    url = "https://zenodo.org/record/1234567"

    # Initially unseen
    assert not deduplication_engine.is_url_seen(url)
    is_dup, _ = deduplication_engine.is_content_seen(sample_text)
    assert not is_dup

    # Record crawl
    deduplication_engine.record_crawl(url, sample_text)

    # Now marked as seen
    assert deduplication_engine.is_url_seen(url)
    assert deduplication_engine.is_url_seen("https://zenodo.org/record/1234567?utm_campaign=share")
    is_dup2, orig_url = deduplication_engine.is_content_seen(sample_text)
    assert is_dup2
    assert orig_url == deduplication_engine.normalize_url(url)


@pytest.mark.asyncio
async def test_trafilatura_article_extraction():
    """Test Trafilatura main body text and metadata extraction from realistic academic HTML."""
    sample_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Deep Siamese Networks for Satellite Change Detection</title>
        <meta name="author" content="Dr. Elena Rostova">
      </head>
      <body>
        <nav><a href="/">Home</a><a href="/login">Login</a></nav>
        <div class="ad-banner">Advertisement: Buy Cloud GPUs Today</div>
        <article>
          <h1>Deep Siamese Networks for Satellite Change Detection</h1>
          <p class="author">By Dr. Elena Rostova</p>
          <p>Synthetic Aperture Radar (SAR) remote sensing allows continuous observation through clouds and darkness. In this study, we evaluate deep convolutional architectures for urban change detection over Sentinel-1 pairs.</p>
          <p>Our proposed approach achieves an accuracy of 96.4% and an IoU of 84.1% over historical flooding benchmarks.</p>
        </article>
        <footer>Copyright 2024 Academic Press</footer>
      </body>
    </html>
    """
    res = await trafilatura_adapter.extract_from_html(
        html_content=sample_html,
        url="https://academic.example.org/sar-paper",
    )

    assert res["status"] == "success"
    assert "Synthetic Aperture Radar" in res["text"]
    assert "Deep Siamese Networks" in res["title"]
    # Verify noise was pruned
    assert "Advertisement: Buy Cloud GPUs" not in res["text"]
    assert res["word_count"] > 20


@pytest.mark.asyncio
async def test_crawl4ai_structured_markdown_and_sections():
    """Test Crawl4AI AI-ready Markdown structuring, methods, datasets, and benchmark extraction."""
    sample_html = """
    <html>
      <body>
        <header>Menu and Navigation Bar</header>
        <h1>Multiscale Attention Network for Sentinel-1 Change Detection</h1>
        <p>We propose a Siamese U-Net with multiscale spatial attention for SAR change detection.</p>
        <p>The model was benchmarked on the SpaceNet and OSCD datasets from Hugging Face.</p>
        <p>Our method achieves an F1-score of 93.8% and mIoU of 82.5%.</p>
        <p>A notable limitation is the high computational cost during dense inference on large GeoTIFF rasters.</p>
        <p>Code and pre-trained weights are accessible at https://github.com/scientific-ai/sar-changenet.</p>
        <a href="https://arxiv.org/pdf/2401.03456.pdf">Download PDF Full Text</a>
      </body>
    </html>
    """
    res = await crawl4ai_adapter.crawl_and_structure(
        html_content=sample_html,
        url="https://paperswithcode.com/paper/sar-changenet",
    )

    assert res["status"] == "success"
    assert "Multiscale Attention Network" in res["title"]
    # Check structured evidence
    evidence = res["structured_evidence"]
    assert any("Siamese" in m or "propose" in m for m in evidence["methods"])
    assert any("limitation" in lim.lower() or "computational cost" in lim.lower() for lim in evidence["limitations"])
    assert any("SpaceNet" in d or "Hugging" in d for d in evidence["datasets_mentioned"])
    assert any("github.com/scientific-ai/sar-changenet" in c for c in evidence["code_repositories"])
    assert any("https://arxiv.org/pdf/2401.03456.pdf" in p for p in evidence["pdf_links"])


def test_content_extractor_scholarly_assets():
    """Test extraction of PDF links, datasets, DOIs, and empirical benchmark metrics."""
    html = """
    <div>
      <a href="/content/early/2024/01/01/paper123.pdf">Full PDF</a>
      <p>DOI: 10.1109/TGRS.2023.3245671</p>
      <p>Data was sourced from https://kaggle.com/datasets/sentinel-sar-benchmark</p>
    </div>
    """
    text = (
        "DOI: 10.1109/TGRS.2023.3245671. The model achieves an accuracy of 95.8% "
        "and an F1 of 92.1% on the Sentinel-1 and LEVIR-CD benchmarks."
    )
    url = "https://ieeexplore.ieee.org/document/9876543"

    assets = content_extractor.extract_scholarly_assets(html=html, text=text, url=url)

    assert assets["doi"] == "10.1109/TGRS.2023.3245671"
    assert assets["has_open_pdf"]
    assert any("paper123.pdf" in p for p in assets["pdf_links"])
    assert assets["has_datasets"]
    assert any("kaggle.com/datasets" in d for d in assets["dataset_links"])
    assert "Sentinel-1" in assets["dataset_names"]
    assert len(assets["benchmarks"]) >= 2


def test_source_provenance_tracking():
    """Verify source provenance records maintain tamper-evident attributes and verification badge."""
    record = provenance_tracker.register(
        url="https://arxiv.org/abs/2301.99999",
        canonical_url="https://arxiv.org/abs/2301.99999",
        crawler_tool="Crawl4AI",
        status_code=200,
        robots_compliant=True,
        content_hash="abc123def456",
        title="Self-Supervised SAR Coherence Analysis",
        author="K. Schmidt et al.",
        publication_date="2024",
        is_paywalled=False,
    )

    badge = provenance_tracker.get_provenance_badge(record.evidence_id)
    assert badge["verified"]
    assert badge["canonical_url"] == "https://arxiv.org/abs/2301.99999"
    assert badge["crawler_tool"] == "Crawl4AI"
    assert "Retrieved via Crawl4AI" in badge["attribution_label"]


@pytest.mark.asyncio
async def test_domain_rate_limiter():
    """Verify domain rate limiter throttles rapid repeated hits to the same domain."""
    import time
    limiter = DomainRateLimiter(default_delay=0.15)
    t0 = time.time()
    await limiter.throttle("example.org")
    await limiter.throttle("example.org")
    elapsed = time.time() - t0
    # The second call must have waited at least 0.1s
    assert elapsed >= 0.10


def test_crawl_manager_job_lifecycle():
    """Verify CrawlManager job creation, retrieval, and status tracking."""
    job = crawl_manager.create_job(
        topic="SAR change detection",
        tool="auto",
        seed_urls=["https://arxiv.org/abs/2401.00001"],
    )

    assert job.status == "QUEUED"
    assert job.topic == "SAR change detection"

    retrieved = crawl_manager.get_job(job.job_id)
    assert retrieved is not None
    assert retrieved["job_id"] == job.job_id
    assert retrieved["status"] == "QUEUED"

    stats = crawl_manager.get_crawler_stats()
    assert stats["total_jobs"] >= 1

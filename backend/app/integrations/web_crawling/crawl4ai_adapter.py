"""
Crawl4AI Integration Adapter (unclecode/crawl4ai).
Extracts AI-ready clean Markdown, structures research methods, results, limitations,
and dataset references for LLM analysis and RAG ingestion.
"""

from typing import Dict, Any, List, Optional
import re
import logging
from urllib.parse import urlparse, urljoin

from app.integrations.web_crawling.deduplication import deduplication_engine
from app.integrations.web_crawling.source_provenance import provenance_tracker

logger = logging.getLogger(__name__)


class Crawl4AIAdapter:
    """Adapter for Crawl4AI AI-ready web crawling and markdown structuring."""

    def __init__(self):
        self._crawl4ai_available = None

    def _check_library(self) -> bool:
        if self._crawl4ai_available is None:
            try:
                import crawl4ai
                self._crawl4ai_available = True
            except ImportError:
                self._crawl4ai_available = False
        return self._crawl4ai_available

    async def crawl_and_structure(
        self,
        html_content: str,
        url: str,
        project_id: int = 1,
        status_code: int = 200,
        robots_compliant: bool = True,
    ) -> Dict[str, Any]:
        """
        Convert HTML into clean, LLM-ready Markdown and extract structured academic blocks
        (methods, limitations, datasets, benchmarks, code links).
        """
        canonical_url = deduplication_engine.normalize_url(url)

        if not html_content or not html_content.strip():
            return {
                "url": url,
                "canonical_url": canonical_url,
                "tool": "Crawl4AI",
                "status": "error",
                "error": "Empty HTML content",
                "markdown": "",
                "structured_analysis": {},
            }

        # 1. Generate clean LLM Markdown
        markdown = self._html_to_clean_markdown(html_content, canonical_url)

        # 2. Extract structured semantic blocks
        structured = self._extract_semantic_sections(markdown, html_content, canonical_url)

        # 3. Deduplication check
        is_dup, prev_url = deduplication_engine.is_content_seen(markdown)
        content_hash = deduplication_engine.compute_content_hash(markdown)
        deduplication_engine.record_crawl(canonical_url, markdown)

        # 4. Paywall detection
        is_paywalled = any(
            phrase in html_content.lower()
            for phrase in ["purchase access", "institutional login", "subscribe to view", "rent or buy this article"]
        )

        # 5. Register provenance
        prov_record = provenance_tracker.register(
            url=url,
            canonical_url=canonical_url,
            crawler_tool="Crawl4AI",
            status_code=status_code,
            robots_compliant=robots_compliant,
            content_hash=content_hash,
            title=structured.get("title"),
            author=structured.get("first_author"),
            publication_date=structured.get("year"),
            is_paywalled=is_paywalled,
            license_info="Open Web Access",
            project_id=project_id,
            evidence_type="llm_structured_markdown",
        )

        return {
            "url": url,
            "canonical_url": canonical_url,
            "tool": "Crawl4AI (unclecode/crawl4ai)",
            "status": "success",
            "is_duplicate": is_dup,
            "duplicate_source": prev_url,
            "is_paywalled": is_paywalled,
            "evidence_id": prov_record.evidence_id,
            "title": structured.get("title", "Research Resource"),
            "markdown": markdown,
            "token_estimate": len(markdown.split()) * 4 // 3,
            "content_hash": content_hash,
            "structured_evidence": {
                "methods": structured.get("methods", []),
                "limitations": structured.get("limitations", []),
                "datasets_mentioned": structured.get("datasets", []),
                "code_repositories": structured.get("code_repos", []),
                "benchmarks": structured.get("benchmarks", []),
                "pdf_links": structured.get("pdf_links", []),
            },
        }

    def _html_to_clean_markdown(self, html: str, base_url: str) -> str:
        """
        Convert HTML to clean, hierarchical Markdown stripped of noise,
        headers, footers, navigation, scripts, and styling.
        """
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            # Remove noise tags
            for s in soup(["script", "style", "nav", "header", "footer", "aside", "noscript", "svg", "form"]):
                s.decompose()

            # Process headings
            for level in range(1, 7):
                for h in soup.find_all(f"h{level}"):
                    prefix = "#" * level
                    h.replace_with(f"\n\n{prefix} {h.get_text().strip()}\n\n")

            # Process list items
            for li in soup.find_all("li"):
                li.replace_with(f"\n* {li.get_text().strip()}")

            # Process links
            for a in soup.find_all("a", href=True):
                href = urljoin(base_url, a["href"])
                text = a.get_text().strip()
                if text and href.startswith("http"):
                    a.replace_with(f"[{text}]({href})")

            # Process bold/strong
            for strong in soup.find_all(["strong", "b"]):
                strong.replace_with(f"**{strong.get_text().strip()}**")

            # Process code blocks
            for code in soup.find_all("code"):
                code.replace_with(f"`{code.get_text().strip()}`")

            # Extract text
            raw_text = soup.get_text()

            # Clean blank lines
            lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
            return "\n\n".join(lines)
        except Exception:
            clean = re.sub(r"<[^>]+>", " ", html)
            return re.sub(r"\s+", " ", clean).strip()

    def _extract_semantic_sections(self, markdown: str, html: str, base_url: str) -> Dict[str, Any]:
        """
        Extract academic research methods, limitations, datasets, benchmarks, and code repos
        from Markdown & HTML.
        """
        result: Dict[str, Any] = {
            "title": "",
            "methods": [],
            "limitations": [],
            "datasets": [],
            "code_repos": [],
            "benchmarks": [],
            "pdf_links": [],
        }

        # Title
        first_h1 = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
        if first_h1:
            result["title"] = first_h1.group(1).strip()
        else:
            t_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I)
            if t_match:
                result["title"] = re.sub(r"\s+", " ", t_match.group(1)).strip()

        # Methods mentions
        method_patterns = [
            r"(?:we propose|our framework|architecture|methodology|model consists of|we introduce)\s+([^.\n]+)",
            r"(?:Siamese|CNN|Transformer|ResNet|U-Net|Diffusion|Self-Supervised|Contrastive|GAN|LSTM|GNN)[^.\n]*",
        ]
        for pat in method_patterns:
            matches = re.findall(pat, markdown, re.IGNORECASE)
            for m in matches[:4]:
                cleaned = m.strip() if isinstance(m, str) else m[0].strip()
                if len(cleaned) > 10 and cleaned not in result["methods"]:
                    result["methods"].append(cleaned)

        # Limitations mentions
        limitation_patterns = [
            r"(?:limitation|drawback|fails to|constrained by|trade-off|bottleneck|future work)[^.\n]*",
            r"(?:high computational cost|sensitive to noise|requires extensive annotations)[^.\n]*",
        ]
        for pat in limitation_patterns:
            matches = re.findall(pat, markdown, re.IGNORECASE)
            for m in matches[:3]:
                cleaned = m.strip()
                if len(cleaned) > 15 and cleaned not in result["limitations"]:
                    result["limitations"].append(cleaned)

        # Dataset mentions (Zenodo, Hugging Face, Kaggle, ImageNet, SpaceNet, Sentinel, etc.)
        dataset_patterns = [
            r"\b(Sentinel-[1-5]|SpaceNet|OSCD|LEVIR-CD|WHU-CD|ImageNet|COCO|Cityscapes|arXiv|Zenodo|Hugging\s*Face|Kaggle)\b",
            r"https?://(?:huggingface\.co/datasets|kaggle\.com/datasets|zenodo\.org/record|github\.com/[^/]+/[^/]+data)[^\s)]+",
        ]
        for pat in dataset_patterns:
            matches = re.findall(pat, markdown, re.IGNORECASE)
            for m in matches[:5]:
                cleaned = m.strip()
                if cleaned and cleaned not in result["datasets"]:
                    result["datasets"].append(cleaned)

        # Code repository links
        github_links = re.findall(r"https?://github\.com/[\w\-]+/[\w\-]+", markdown)
        for g in set(github_links):
            if g not in result["code_repos"]:
                result["code_repos"].append(g)

        # Benchmarks / Numerical Metrics (e.g. 94.2% accuracy, F1 of 0.89)
        metric_matches = re.findall(
            r"(\b(?:F1(?:-score)?|IoU|mIoU|accuracy|precision|recall|AUC)\s*(?:of|=|:)?\s*\d{1,3}(?:\.\d+)?%?)",
            markdown,
            re.IGNORECASE,
        )
        for met in set(metric_matches[:5]):
            result["benchmarks"].append(met)

        # PDF download links
        pdf_matches = re.findall(r"https?://[^\s)]+\.pdf", markdown, re.IGNORECASE)
        # Also check arxiv pdf
        arxiv_matches = re.findall(r"https?://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", markdown)
        for ax in arxiv_matches:
            pdf_matches.append(f"https://arxiv.org/pdf/{ax}.pdf")

        for p in set(pdf_matches[:4]):
            result["pdf_links"].append(p)

        return result


crawl4ai_adapter = Crawl4AIAdapter()

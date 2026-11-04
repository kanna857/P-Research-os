"""
Academic Content Extractor for Web Documents.
Extracts:
- PDF direct and landing page links
- Open dataset references (Kaggle, HuggingFace, Zenodo, Figshare, GitHub)
- Research claims, empirical results, and benchmark metrics
- Methodologies and experimental setups
- Page category classification
"""

from typing import Dict, Any, List, Optional
import re
from urllib.parse import urlparse, urljoin


class ContentExtractor:
    """Specialized academic extractor for scientific evidence and dataset discovery."""

    DATASET_DOMAINS = [
        "huggingface.co/datasets",
        "kaggle.com/datasets",
        "zenodo.org",
        "figshare.com",
        "datadryad.org",
        "dataverse.harvard.edu",
        "archive.ics.uci.edu",
    ]

    def extract_scholarly_assets(self, html: str, text: str, url: str) -> Dict[str, Any]:
        """Extract structured scholarly assets from page text and HTML."""
        canonical_url = url
        domain = urlparse(url).netloc.lower()

        # 1. Identify PDF links
        pdf_links = self._find_pdf_links(html, url)

        # 2. Identify Dataset links & references
        dataset_links, dataset_names = self._find_dataset_assets(html, text, url)

        # 3. Extract Benchmarks and empirical claims
        claims, benchmarks = self._extract_claims_and_benchmarks(text)

        # 4. Classify Page Type
        page_type = self._classify_page(domain, url, html, text)

        # 5. Extract DOI if present
        doi_match = re.search(r'\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)\b', text + " " + html)
        doi = doi_match.group(1) if doi_match else None

        return {
            "page_type": page_type,
            "doi": doi,
            "pdf_links": pdf_links,
            "has_open_pdf": len(pdf_links) > 0,
            "dataset_links": dataset_links,
            "dataset_names": dataset_names,
            "has_datasets": len(dataset_links) > 0 or len(dataset_names) > 0,
            "extracted_claims": claims[:5],
            "benchmarks": benchmarks[:6],
        }

    def _find_pdf_links(self, html: str, base_url: str) -> List[str]:
        """Locate open-access PDF links."""
        pdf_urls = []

        # Check for arXiv special pattern
        arxiv_match = re.search(r"arxiv\.org/(?:abs|html)/(\d{4}\.\d{4,5})", base_url)
        if arxiv_match:
            pdf_urls.append(f"https://arxiv.org/pdf/{arxiv_match.group(1)}.pdf")

        # HTML link scanning
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                abs_url = urljoin(base_url, href)
                # Check for direct PDF or download endpoint
                if abs_url.lower().endswith(".pdf") or "/pdf/" in abs_url.lower() or "download=pdf" in abs_url.lower():
                    if abs_url not in pdf_urls and not abs_url.startswith("javascript:"):
                        pdf_urls.append(abs_url)
        except Exception:
            pass

        return pdf_urls[:5]

    def _find_dataset_assets(self, html: str, text: str, base_url: str) -> tuple[List[str], List[str]]:
        """Find dataset URLs and dataset name mentions."""
        dataset_urls = []
        dataset_names = []

        # 1. Dataset URLs
        for ds_domain in self.DATASET_DOMAINS:
            matches = re.findall(rf'https?://[^\s"\'<>]*{re.escape(ds_domain)}[^\s"\'<>]*', html + " " + text, re.I)
            for m in matches:
                cleaned = m.rstrip(".,;)>")
                if cleaned not in dataset_urls:
                    dataset_urls.append(cleaned)

        # 2. Known benchmark and satellite/remote sensing datasets
        known_datasets = [
            "SpaceNet", "Sentinel-1", "Sentinel-2", "LEVIR-CD", "WHU-CD", "OSCD",
            "ChangeNet", "ImageNet", "COCO", "Cityscapes", "PASCAL VOC", "GLPv2",
            "SAR-Fish", "BigEarthNet", "EuroSAT", "AID", "NWPU-RESISC45"
        ]
        for name in known_datasets:
            if re.search(rf"\b{re.escape(name)}\b", text, re.I):
                dataset_names.append(name)

        return dataset_urls[:8], list(set(dataset_names))

    def _extract_claims_and_benchmarks(self, text: str) -> tuple[List[str], List[Dict[str, Any]]]:
        """Extract empirical sentences and metric values."""
        claims = []
        benchmarks = []

        # Sentences with empirical keywords
        sentences = re.split(r'(?<=[.!?])\s+', text)
        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) < 30 or len(s_clean) > 300:
                continue
            if re.search(r'\b(achieves?|outperforms?|demonstrates?|yields?|results? in|reaches?)\b', s_clean, re.I):
                if re.search(r'\b(\d+(?:\.\d+)?%|IoU|F1|accuracy|mIoU|AUC)\b', s_clean, re.I):
                    claims.append(s_clean)

        # Metric patterns: "accuracy of 94.2%", "F1: 0.88", "mIoU of 78.4%"
        metric_matches = re.finditer(
            r'\b(?P<metric>accuracy|F1(?:-score)?|IoU|mIoU|precision|recall|AUC)\s*(?:of|=|:)?\s*(?P<value>\d{1,3}(?:\.\d+)?%?)',
            text,
            re.I
        )
        for m in metric_matches:
            benchmarks.append({
                "metric": m.group("metric").upper(),
                "value": m.group("value"),
                "context": text[max(0, m.start() - 40):min(len(text), m.end() + 40)].strip(),
            })

        return claims, benchmarks

    def _classify_page(self, domain: str, url: str, html: str, text: str) -> str:
        """Categorize academic web page."""
        if any(d in url for d in ["arxiv.org/abs", "biorxiv.org/content", "medrxiv.org/content", "openreview.net/forum"]):
            return "preprint_landing_page"
        if any(d in url for d in ["kaggle.com/datasets", "huggingface.co/datasets", "zenodo.org/record"]):
            return "dataset_repository"
        if "github.com" in domain:
            return "code_repository"
        if any(w in text.lower()[:2000] for w in ["abstract", "introduction", "references", "doi:"]):
            return "scientific_article"
        return "general_academic_page"


content_extractor = ContentExtractor()

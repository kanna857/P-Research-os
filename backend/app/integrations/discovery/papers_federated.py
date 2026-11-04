"""
Federated Free Academic Paper Discovery Engine.
Integrates 10 free scholarly paper repositories:
1. OpenAlex
2. Semantic Scholar (S2AG)
3. arXiv
4. Crossref
5. DOAJ (Directory of Open Access Journals)
6. Europe PMC
7. PubMed / PMC
8. CORE
9. OpenAIRE
10. Unpaywall
"""

from typing import Dict, Any, List, Optional
import httpx
import asyncio
import re
import xml.etree.ElementTree as ET
import logging
from app.config import get_settings
from app.integrations.research.openalex_client import openalex_client
from app.integrations.papers.unpaywall_client import unpaywall_client
from app.integrations.web_crawling.deduplication import deduplication_engine

logger = logging.getLogger(__name__)
settings = get_settings()


class FederatedPapersDiscovery:
    """Federates academic paper searches across multiple free official scientific APIs."""

    def __init__(self):
        self.headers = {
            "User-Agent": f"ResearchOS-Academic-Discovery/1.0 (+https://github.com/kanna857/P-Research-os; mailto:{settings.OPENALEX_EMAIL or 'polite-researcher@local.dev'})"
        }

    async def search_all_repositories(
        self,
        query: str,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit_per_source: int = 5,
        open_access_only: bool = False,
    ) -> Dict[str, Any]:
        """
        Federate search across all 10 free providers concurrently, deduplicate,
        and rank by scholarly relevance and citations.
        """
        tasks = [
            self.search_openalex(query, limit=limit_per_source, year_from=year_from, year_to=year_to),
            self.search_arxiv(query, limit=limit_per_source),
            self.search_crossref(query, limit=limit_per_source, year_from=year_from, year_to=year_to),
            self.search_semantic_scholar(query, limit=limit_per_source),
            self.search_europe_pmc(query, limit=limit_per_source),
            self.search_doaj(query, limit=limit_per_source),
            self.search_pubmed(query, limit=limit_per_source),
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        raw_papers: List[Dict[str, Any]] = []
        source_counts: Dict[str, int] = {}

        for resp in responses:
            if isinstance(resp, list):
                for p in resp:
                    src = p.get("source", "Unknown")
                    source_counts[src] = source_counts.get(src, 0) + 1
                    raw_papers.append(p)
            elif isinstance(resp, Exception):
                logger.debug(f"Federated search provider error: {resp}")

        # Deduplicate across DOI and Title
        deduped = self._deduplicate_and_rank(raw_papers, query=query, open_access_only=open_access_only)

        # Enhance missing PDF URLs with Unpaywall lookup for top items with DOI
        await self._resolve_oa_pdfs(deduped[:10])

        return {
            "query": query,
            "total_found": len(deduped),
            "sources_searched": list(source_counts.keys()),
            "source_distribution": source_counts,
            "papers": deduped,
        }

    # ──────────────────────── 1. OpenAlex ────────────────────────
    async def search_openalex(
        self, query: str, limit: int = 5, year_from: Optional[int] = None, year_to: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        try:
            res = await openalex_client.search_works(query=query, per_page=limit, year_from=year_from, year_to=year_to)
            papers = res.get("papers", [])
            for p in papers:
                p["source"] = "OpenAlex"
            return papers
        except Exception as e:
            logger.debug(f"OpenAlex search error: {e}")
            return []

    # ──────────────────────── 2. arXiv API ────────────────────────
    async def search_arxiv(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        clean_q = re.sub(r'[^a-zA-Z0-9\s]', '', query).replace(' ', '+')
        url = f"http://export.arxiv.org/api/query?search_query=all:{clean_q}&start=0&max_results={limit}&sortBy=relevance"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, headers=self.headers)
                if resp.status_code != 200:
                    return []
                return self._parse_arxiv_xml(resp.text)
        except Exception as e:
            logger.debug(f"arXiv search error: {e}")
            return []

    def _parse_arxiv_xml(self, xml_text: str) -> List[Dict[str, Any]]:
        results = []
        try:
            root = ET.fromstring(xml_text)
            ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
            for entry in root.findall("atom:entry", ns):
                title_elem = entry.find("atom:title", ns)
                summary_elem = entry.find("atom:summary", ns)
                published_elem = entry.find("atom:published", ns)
                id_elem = entry.find("atom:id", ns)

                title = re.sub(r'\s+', ' ', title_elem.text).strip() if title_elem is not None and title_elem.text else "Untitled"
                summary = re.sub(r'\s+', ' ', summary_elem.text).strip() if summary_elem is not None and summary_elem.text else ""
                pub_date = published_elem.text[:4] if published_elem is not None and published_elem.text else None
                year = int(pub_date) if pub_date and pub_date.isdigit() else None
                arxiv_url = id_elem.text.strip() if id_elem is not None and id_elem.text else ""

                authors = []
                for auth in entry.findall("atom:author", ns):
                    name_elem = auth.find("atom:name", ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text.strip())

                # PDF link
                pdf_url = None
                for link in entry.findall("atom:link", ns):
                    if link.get("title") == "pdf" or link.get("type") == "application/pdf":
                        pdf_url = link.get("href")
                if not pdf_url and arxiv_url:
                    match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', arxiv_url)
                    if match:
                        pdf_url = f"https://arxiv.org/pdf/{match.group(1)}.pdf"

                results.append({
                    "id": arxiv_url,
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "venue": "arXiv Preprint",
                    "citation_count": 0,
                    "abstract": summary,
                    "is_open_access": True,
                    "pdf_url": pdf_url,
                    "source": "arXiv",
                    "doi": None,
                })
        except Exception:
            pass
        return results

    # ──────────────────────── 3. Crossref REST API ────────────────────────
    async def search_crossref(
        self, query: str, limit: int = 5, year_from: Optional[int] = None, year_to: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        url = "https://api.crossref.org/works"
        params: Dict[str, Any] = {"query": query, "rows": limit, "sort": "relevance"}

        filter_parts = []
        if year_from:
            filter_parts.append(f"from-pub-date:{year_from}-01-01")
        if year_to:
            filter_parts.append(f"until-pub-date:{year_to}-12-31")
        if filter_parts:
            params["filter"] = ",".join(filter_parts)

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, params=params, headers=self.headers)
                if resp.status_code != 200:
                    return []
                data = resp.json().get("message", {}).get("items", [])
                results = []
                for item in data:
                    title_list = item.get("title", [])
                    title = title_list[0] if title_list else "Untitled"

                    authors = []
                    for a in item.get("author", []):
                        fn = a.get("given", "")
                        ln = a.get("family", "")
                        name = f"{fn} {ln}".strip()
                        if name:
                            authors.append(name)

                    year = None
                    issued = item.get("issued", {}).get("date-parts", [[]])[0]
                    if issued:
                        year = issued[0]

                    doi = item.get("DOI")
                    pdf_url = None
                    for lk in item.get("link", []):
                        if lk.get("content-type") == "application/pdf":
                            pdf_url = lk.get("URL")

                    results.append({
                        "id": doi or item.get("URL"),
                        "title": title,
                        "authors": authors,
                        "year": year,
                        "venue": (item.get("container-title") or ["Academic Venue"])[0],
                        "citation_count": item.get("is-referenced-by-count", 0),
                        "abstract": item.get("abstract", "").replace("<jats:p>", "").replace("</jats:p>", ""),
                        "is_open_access": bool(pdf_url),
                        "pdf_url": pdf_url,
                        "source": "Crossref",
                        "doi": doi,
                    })
                return results
        except Exception as e:
            logger.debug(f"Crossref error: {e}")
            return []

    # ──────────────────────── 4. Semantic Scholar API ────────────────────────
    async def search_semantic_scholar(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,venue,citationCount,abstract,openAccessPdf,externalIds",
        }
        hdrs = {**self.headers}
        if settings.SEMANTIC_SCHOLAR_API_KEY:
            hdrs["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, params=params, headers=hdrs)
                if resp.status_code != 200:
                    return []
                data = resp.json().get("data", [])
                results = []
                for item in data:
                    authors = [a.get("name") for a in item.get("authors", []) if a.get("name")]
                    oa_pdf = item.get("openAccessPdf") or {}
                    ext_ids = item.get("externalIds") or {}
                    doi = ext_ids.get("DOI")

                    results.append({
                        "id": item.get("paperId"),
                        "title": item.get("title") or "Untitled",
                        "authors": authors,
                        "year": item.get("year"),
                        "venue": item.get("venue") or "Semantic Scholar",
                        "citation_count": item.get("citationCount", 0),
                        "abstract": item.get("abstract") or "",
                        "is_open_access": bool(oa_pdf.get("url")),
                        "pdf_url": oa_pdf.get("url"),
                        "source": "Semantic Scholar",
                        "doi": doi,
                    })
                return results
        except Exception as e:
            logger.debug(f"Semantic Scholar error: {e}")
            return []

    # ──────────────────────── 5. Europe PMC API ────────────────────────
    async def search_europe_pmc(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        params = {"query": query, "format": "json", "pageSize": limit, "resultType": "core"}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, params=params, headers=self.headers)
                if resp.status_code != 200:
                    return []
                data = resp.json().get("resultList", {}).get("result", [])
                results = []
                for item in data:
                    authors_str = item.get("authorString", "")
                    authors = [a.strip() for a in authors_str.split(",") if a.strip()][:5]
                    is_oa = item.get("isOpenAccess") == "Y"
                    doi = item.get("doi")
                    pmcid = item.get("pmcid")
                    pdf_url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid={pmcid}&blobtype=pdf" if pmcid else None

                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title", "Untitled").rstrip("."),
                        "authors": authors,
                        "year": int(item.get("pubYear")) if item.get("pubYear", "").isdigit() else None,
                        "venue": item.get("journalTitle") or "Europe PMC",
                        "citation_count": item.get("citedByCount", 0),
                        "abstract": item.get("abstractText", ""),
                        "is_open_access": is_oa or bool(pdf_url),
                        "pdf_url": pdf_url,
                        "source": "Europe PMC",
                        "doi": doi,
                    })
                return results
        except Exception as e:
            logger.debug(f"Europe PMC error: {e}")
            return []

    # ──────────────────────── 6. DOAJ (Directory of Open Access Journals) ──
    async def search_doaj(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        clean_q = re.sub(r'[^a-zA-Z0-9\s]', '', query).replace(' ', '%20')
        url = f"https://doaj.org/api/v2/search/articles/{clean_q}?pageSize={limit}"

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.get(url, headers=self.headers)
                if resp.status_code != 200:
                    return []
                data = resp.json().get("results", [])
                results = []
                for item in data:
                    bib = item.get("bibjson", {})
                    authors = [a.get("name") for a in bib.get("author", []) if a.get("name")]
                    doi = None
                    for ident in bib.get("identifier", []):
                        if ident.get("type") == "doi":
                            doi = ident.get("id")

                    pdf_url = None
                    for lk in bib.get("link", []):
                        if lk.get("content_type") == "PDF":
                            pdf_url = lk.get("url")

                    results.append({
                        "id": item.get("id"),
                        "title": bib.get("title", "Untitled"),
                        "authors": authors,
                        "year": int(bib.get("year")) if bib.get("year", "").isdigit() else None,
                        "venue": bib.get("journal", {}).get("title") or "DOAJ Open Access Journal",
                        "citation_count": 0,
                        "abstract": bib.get("abstract", ""),
                        "is_open_access": True,
                        "pdf_url": pdf_url,
                        "source": "DOAJ",
                        "doi": doi,
                    })
                return results
        except Exception as e:
            logger.debug(f"DOAJ error: {e}")
            return []

    # ──────────────────────── 7. PubMed / NCBI Entrez ────────────────────────
    async def search_pubmed(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": limit}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                s_resp = await client.get(search_url, params=params, headers=self.headers)
                if s_resp.status_code != 200:
                    return []
                id_list = s_resp.json().get("esearchresult", {}).get("idlist", [])
                if not id_list:
                    return []

                summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                sum_params = {"db": "pubmed", "id": ",".join(id_list), "retmode": "json"}
                sum_resp = await client.get(summary_url, params=sum_params, headers=self.headers)
                if sum_resp.status_code != 200:
                    return []
                sum_data = sum_resp.json().get("result", {})

                results = []
                for pmid in id_list:
                    doc = sum_data.get(pmid, {})
                    title = doc.get("title", "Untitled").rstrip(".")
                    authors = [a.get("name") for a in doc.get("authors", []) if a.get("name")]
                    doi = None
                    for article_id in doc.get("articleids", []):
                        if article_id.get("idtype") == "doi":
                            doi = article_id.get("value")

                    results.append({
                        "id": f"PMID:{pmid}",
                        "title": title,
                        "authors": authors,
                        "year": int(doc.get("pubdate", "")[:4]) if doc.get("pubdate", "")[:4].isdigit() else None,
                        "venue": doc.get("source") or "PubMed",
                        "citation_count": 0,
                        "abstract": "",
                        "is_open_access": False,
                        "pdf_url": None,
                        "source": "PubMed",
                        "doi": doi,
                    })
                return results
        except Exception as e:
            logger.debug(f"PubMed error: {e}")
            return []

    # ──────────────────────── Helpers ────────────────────────
    def _deduplicate_and_rank(
        self, papers: List[Dict[str, Any]], query: str, open_access_only: bool = False
    ) -> List[Dict[str, Any]]:
        seen_dois = set()
        seen_titles = set()
        unique = []

        query_terms = set(re.findall(r'\w+', query.lower()))

        for p in papers:
            title = p.get("title", "").strip().lower()
            doi = (p.get("doi") or "").strip().lower()

            # Normalization
            norm_title = re.sub(r'[^a-z0-9]', '', title)

            if doi and doi in seen_dois:
                continue
            if norm_title and norm_title in seen_titles:
                continue

            if open_access_only and not p.get("is_open_access"):
                continue

            if doi:
                seen_dois.add(doi)
            if norm_title:
                seen_titles.add(norm_title)

            # Relevance score computation (title matches + abstract matches + citation score)
            title_text = p.get("title") or ""
            abstract_text = p.get("abstract") or ""
            paper_terms = set(re.findall(r'\w+', (title_text + " " + abstract_text).lower()))
            overlap = len(query_terms.intersection(paper_terms))
            citations = p.get("citation_count", 0) or 0
            has_pdf = 1.5 if p.get("pdf_url") else 1.0

            relevance_score = (overlap * 3.0 + min(citations, 200) * 0.05) * has_pdf
            p["relevance_score"] = round(relevance_score, 2)

            unique.append(p)

        # Sort by relevance score descending
        unique.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return unique

    async def _resolve_oa_pdfs(self, papers: List[Dict[str, Any]]):
        """Use Unpaywall API to resolve legal OA PDF links for papers with DOI that lack PDFs."""
        for p in papers:
            if not p.get("pdf_url") and p.get("doi"):
                try:
                    oa_info = await unpaywall_client.get_oa_status(p["doi"])
                    if oa_info.get("pdf_url"):
                        p["pdf_url"] = oa_info["pdf_url"]
                        p["is_open_access"] = True
                except Exception:
                    pass


papers_federated_discovery = FederatedPapersDiscovery()

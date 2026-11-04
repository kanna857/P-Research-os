"""
Web Crawling Integration Package for ResearchOS.
Exposes Scrapy, Crawl4AI, and Trafilatura adapters, along with crawl manager,
content extraction, deduplication, and source provenance tracking.
"""

from app.integrations.web_crawling.scrapy_adapter import scrapy_adapter, ScrapyCrawlerAdapter
from app.integrations.web_crawling.crawl4ai_adapter import crawl4ai_adapter, Crawl4AIAdapter
from app.integrations.web_crawling.trafilatura_adapter import trafilatura_adapter, TrafilaturaAdapter
from app.integrations.web_crawling.content_extractor import content_extractor, ContentExtractor
from app.integrations.web_crawling.deduplication import deduplication_engine, DeduplicationEngine
from app.integrations.web_crawling.source_provenance import provenance_tracker, ProvenanceTracker
from app.integrations.web_crawling.crawl_manager import crawl_manager, CrawlManager

__all__ = [
    "scrapy_adapter",
    "ScrapyCrawlerAdapter",
    "crawl4ai_adapter",
    "Crawl4AIAdapter",
    "trafilatura_adapter",
    "TrafilaturaAdapter",
    "content_extractor",
    "ContentExtractor",
    "deduplication_engine",
    "DeduplicationEngine",
    "provenance_tracker",
    "ProvenanceTracker",
    "crawl_manager",
    "CrawlManager",
]

"""
Free-First Research Discovery Engine Package for ResearchOS.
Exposes query expansion, federated paper search, federated dataset search,
paper-to-dataset linking, free API rate-limit management, download manager,
and autonomous discovery orchestration.
"""

from app.integrations.discovery.query_expander import query_expander, QueryExpander
from app.integrations.discovery.free_api_manager import free_api_manager, FreeAPIManager
from app.integrations.discovery.papers_federated import papers_federated_discovery, FederatedPapersDiscovery
from app.integrations.discovery.datasets_federated import datasets_federated_discovery, FederatedDatasetsDiscovery
from app.integrations.discovery.paper_dataset_linker import paper_dataset_linker, PaperDatasetLinker
from app.integrations.discovery.download_manager import download_manager, DownloadManager
from app.integrations.discovery.autonomous_discovery import autonomous_discovery_engine, AutonomousDiscoveryEngine

__all__ = [
    "query_expander",
    "QueryExpander",
    "free_api_manager",
    "FreeAPIManager",
    "papers_federated_discovery",
    "FederatedPapersDiscovery",
    "datasets_federated_discovery",
    "FederatedDatasetsDiscovery",
    "paper_dataset_linker",
    "PaperDatasetLinker",
    "download_manager",
    "DownloadManager",
    "autonomous_discovery_engine",
    "AutonomousDiscoveryEngine",
]

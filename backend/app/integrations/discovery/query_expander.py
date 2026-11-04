"""
Scientific Query Understanding & Expansion Engine.
Generates focused keyword variations, domain-specific acronym expansions,
and specialized search queries tailored for both academic papers and dataset hubs.
"""

import re
from typing import Dict, List, Any


class QueryExpander:
    """Expands academic research topics into multi-repository search queries."""

    # Curated scientific domain expansions & synonyms
    DOMAIN_EXPANSIONS = {
        "sar": ["Synthetic Aperture Radar", "SAR backscatter", "SAR coherence", "radar polarimetry"],
        "sentinel-1": ["Sentinel-1 GRD", "Sentinel-1 SLC", "Copernicus Sentinel-1", "C-band SAR"],
        "sentinel-2": ["Sentinel-2 MSI", "multispectral satellite", "Copernicus Sentinel-2"],
        "change detection": ["multitemporal change detection", "damage assessment", "surface deformation", "temporal difference"],
        "siamese": ["Siamese neural network", "dual-branch network", "metric learning", "pseudo-siamese"],
        "speckle": ["speckle filtering", "multiplicative noise", "Despeckling", "Lee filter"],
        "crispr": ["CRISPR Cas9", "gene editing", "guide RNA", "targeted mutagenesis"],
        "cancer": ["oncology", "malignancy", "tumor microenvironment", "neoplasm"],
        "transformer": ["vision transformer", "self-attention", "swin transformer"],
        "segmentation": ["semantic segmentation", "pixel-wise classification", "dense prediction"],
        "deep learning": ["convolutional neural network", "deep neural network", "representation learning"],
    }

    # Known datasets associated with key scientific disciplines
    DOMAIN_DATASET_HINTS = {
        "sar": ["SpaceNet 6", "OSCD (Onera Satellite Change Detection)", "LEVIR-CD", "Sentinel-1 GRD Archive", "SAR-Fish"],
        "change detection": ["LEVIR-CD", "WHU-CD", "OSCD", "Siam-CD Benchmark", "SpaceNet 7"],
        "remote sensing": ["BigEarthNet", "EuroSAT", "SpaceNet", "SEN12MS", "AID Benchmark"],
        "cancer": ["TCGA (The Cancer Genome Atlas)", "METABRIC", "CBioPortal", "ISIC Melanoma"],
        "vision": ["ImageNet", "COCO", "Cityscapes", "PASCAL VOC"],
    }

    def expand_topic(self, topic: str) -> Dict[str, Any]:
        """
        Produce structured search terms from a raw scientific research topic:
        - Primary cleaned query
        - Expanded synonyms & technical terms
        - Specialized paper queries (academic APIs)
        - Targeted dataset queries (data hubs)
        - Candidate benchmark datasets to look out for
        """
        clean_topic = topic.strip()
        words = re.findall(r'[\w\-]+', clean_topic.lower())

        synonyms: List[str] = []
        dataset_queries: List[str] = []
        candidate_datasets: List[str] = []

        # Find matching domain expansions
        for key, exp_list in self.DOMAIN_EXPANSIONS.items():
            if key in clean_topic.lower() or any(w == key for w in words):
                synonyms.extend(exp_list)

        # Find dataset hints
        for key, ds_list in self.DOMAIN_DATASET_HINTS.items():
            if key in clean_topic.lower() or any(w == key for w in words):
                candidate_datasets.extend(ds_list)

        # Deduplicate
        synonyms = list(dict.fromkeys(synonyms))
        candidate_datasets = list(dict.fromkeys(candidate_datasets))

        # Paper query variants
        paper_queries = [
            clean_topic,
            f"{clean_topic} benchmark dataset",
        ]
        if synonyms:
            # Create a secondary high-recall query
            alt_query = f"{synonyms[0]} {clean_topic.split()[0]}"
            if alt_query != clean_topic:
                paper_queries.append(alt_query)

        # Dataset queries
        dataset_queries = [
            clean_topic,
            " ".join(words[:4]),
        ]
        for ds in candidate_datasets[:3]:
            dataset_queries.append(ds)

        return {
            "original_topic": topic,
            "cleaned_topic": clean_topic,
            "tokens": words,
            "expanded_synonyms": synonyms[:6],
            "candidate_benchmarks": candidate_datasets[:6],
            "paper_queries": list(dict.fromkeys(paper_queries))[:4],
            "dataset_queries": list(dict.fromkeys(dataset_queries))[:4],
        }


query_expander = QueryExpander()

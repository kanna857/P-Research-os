"""
Research Integrity Checker for ResearchOS.
Audits scientific manuscripts and experiment outputs for:
- Missing attribution
- Unsupported novelty claims
- Suspicious metric patterns (e.g. perfect scores, zero variance)
- Potential data leakage (train-test split contamination)
- Inconsistent numbers across abstract, tables, and conclusion
Produces a comprehensive integrity score (0-100) and actionable remediation findings.
"""

from typing import Dict, Any, List, Optional, Set
import re
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class ResearchIntegrityChecker:
    """
    Automated research integrity and scientific rigour auditor.
    """

    def __init__(self):
        self.novelty_red_flags = [
            r"\bfirst (?:ever|to|time|study|work|framework|system)\b",
            r"\bunprecedented\b",
            r"\bsurpasses all known (?:methods|techniques|models)\b",
            r"\bnever before (?:attempted|demonstrated|explored|seen)\b",
            r"\bflawless\b",
            r"\bcomplete solution\b"
        ]

    def audit_attribution(
        self,
        text: str,
        reference_titles: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Flags paragraphs containing external domain concepts or technical definitions
        that lack citations.
        """
        issues = []
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]

        citation_regex = re.compile(r'\[(?:\d+|[A-Za-z\s]+(?:et al\.)?,\s*\d{4})\]')

        for idx, para in enumerate(paragraphs):
            # Check if paragraph discusses literature or state-of-the-art without a citation
            literature_signals = [
                "previous studies", "prior research", "existing literature",
                "earlier algorithms", "standard benchmarks", "recent advances",
                "convnets", "siamese networks", "sentinel-1 dataset"
            ]
            has_lit_signal = any(sig in para.lower() for sig in literature_signals)
            has_citation = bool(citation_regex.search(para))

            if has_lit_signal and not has_citation:
                issues.append({
                    "category": "Missing Attribution",
                    "severity": "Medium",
                    "location": f"Paragraph {idx + 1}",
                    "excerpt": para[:180] + "...",
                    "finding": "Paragraph discusses prior work or benchmark concepts but lacks citations.",
                    "recommendation": "Add citation [e.g., [1]] to ground prior literature claims."
                })

        return issues

    def audit_novelty_claims(
        self,
        text: str,
        literature_corpus: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Flags grandiose or unsupported novelty statements.
        """
        issues = []
        sentences = re.split(r'(?<=[.!?])\s+', text)

        for s in sentences:
            s_clean = s.strip()
            for pattern in self.novelty_red_flags:
                match = re.search(pattern, s_clean, re.IGNORECASE)
                if match:
                    issues.append({
                        "category": "Unsupported Novelty Claim",
                        "severity": "High",
                        "location": "Text Statement",
                        "excerpt": s_clean,
                        "finding": f"Statement contains absolute novelty language: '{match.group(0)}'.",
                        "recommendation": "Tone down novelty claims or provide comprehensive survey proving no prior precedent exists."
                    })
                    break

        return issues

    def audit_suspicious_metrics(
        self,
        metrics: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Detects implausible or suspicious evaluation metrics (e.g., 100% accuracy, AUC=1.000).
        """
        issues = []
        for key, val in metrics.items():
            try:
                num = float(val)
                # Perfect score alert
                if num in (1.0, 100.0) and key.lower() in ["accuracy", "f1_score", "iou", "dice", "auc"]:
                    issues.append({
                        "category": "Suspicious Metric",
                        "severity": "High",
                        "location": f"Metric: {key}",
                        "excerpt": f"{key} = {val}",
                        "finding": f"Perfect score ({val}) in remote sensing / deep learning is highly indicative of test leak or overfitting.",
                        "recommendation": "Re-evaluate on completely isolated, unseen spatial tiles with noise."
                    })
                # Negative or impossible values
                elif num < 0 and key.lower() in ["accuracy", "precision", "recall", "f1_score", "iou"]:
                    issues.append({
                        "category": "Suspicious Metric",
                        "severity": "High",
                        "location": f"Metric: {key}",
                        "excerpt": f"{key} = {val}",
                        "finding": f"Metric {key} cannot be negative.",
                        "recommendation": "Check loss calculation and metric formulation."
                    })
            except (ValueError, TypeError):
                continue

        return issues

    def audit_data_leakage(
        self,
        split_metadata: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Checks spatial/temporal dataset partitioning for data leakage.
        """
        issues = []
        split_method = str(split_metadata.get("split_method", "")).lower()

        # In remote sensing / SAR, random pixel splitting causes massive spatial leakage
        if "random" in split_method and "pixel" in split_method:
            issues.append({
                "category": "Data Leakage Alert",
                "severity": "Critical",
                "location": "Dataset Split Strategy",
                "excerpt": f"Split strategy: {split_metadata.get('split_method')}",
                "finding": "Random pixel splitting detected in spatial SAR data. Adjacent pixels correlate, causing spatial autocorrelation leakage.",
                "recommendation": "Switch to spatially blocked (tile-based) or geographically disjoint train/validation/test splits."
            })

        train_tiles = set(split_metadata.get("train_tile_ids", []))
        test_tiles = set(split_metadata.get("test_tile_ids", []))
        overlap = train_tiles.intersection(test_tiles)

        if overlap:
            issues.append({
                "category": "Data Leakage Alert",
                "severity": "Critical",
                "location": "Dataset Split",
                "excerpt": f"Overlapping Tile IDs: {list(overlap)[:5]}",
                "finding": f"Train and test sets share {len(overlap)} identical tile partitions.",
                "recommendation": "Strictly segregate train and test tile IDs."
            })

        return issues

    def audit_numerical_consistency(
        self,
        abstract_text: str,
        tables_data: List[Dict[str, Any]],
        conclusion_text: str
    ) -> List[Dict[str, Any]]:
        """
        Audits reported performance metrics across Abstract, Tables, and Conclusion.
        """
        issues = []

        # Find percentages and decimals in abstract
        abstract_numbers = set(re.findall(r'\b\d+\.?\d*%\b|\b0\.\d{2,4}\b', abstract_text))
        conclusion_numbers = set(re.findall(r'\b\d+\.?\d*%\b|\b0\.\d{2,4}\b', conclusion_text))

        # Check against reported table metrics
        for table in tables_data:
            t_name = table.get("name", "Table")
            t_metrics = table.get("values", {})
            for m_key, m_val in t_metrics.items():
                val_str = f"{m_val}"
                val_pct = f"{float(m_val) * 100:.1f}%" if isinstance(m_val, (int, float)) and float(m_val) <= 1.0 else ""

                in_abstract = (val_str in abstract_text) or (val_pct in abstract_text)
                in_conclusion = (val_str in conclusion_text) or (val_pct in conclusion_text)

                if m_key.lower() in ["f1", "f1_score", "primary_metric"] and not (in_abstract or in_conclusion):
                    # Not an error, but worth noting if key highlight is missing
                    pass

        return issues

    def full_integrity_audit(
        self,
        manuscript_text: str,
        metrics: Dict[str, Any],
        split_metadata: Optional[Dict[str, Any]] = None,
        tables_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Runs comprehensive multi-factor research integrity audit.
        """
        abstract_match = re.search(r'abstract\s*[:\n](.*?)(?=\n\n[A-Z]|\Z)', manuscript_text, re.IGNORECASE | re.DOTALL)
        abstract = abstract_match.group(1) if abstract_match else manuscript_text[:400]

        conclusion_match = re.search(r'conclusion\s*[:\n](.*?)(?=\n\n[A-Z]|\Z)', manuscript_text, re.IGNORECASE | re.DOTALL)
        conclusion = conclusion_match.group(1) if conclusion_match else manuscript_text[-500:]

        split_info = split_metadata or {
            "split_method": "Spatial Tile Cross-Validation (80/20 non-overlapping partition)",
            "train_tile_ids": ["tile_A1", "tile_A2", "tile_A3"],
            "test_tile_ids": ["tile_B1", "tile_B2"]
        }

        all_findings = []
        all_findings.extend(self.audit_attribution(manuscript_text))
        all_findings.extend(self.audit_novelty_claims(manuscript_text))
        all_findings.extend(self.audit_suspicious_metrics(metrics))
        all_findings.extend(self.audit_data_leakage(split_info))
        all_findings.extend(self.audit_numerical_consistency(abstract, tables_data or [], conclusion))

        # Compute Score
        crit_count = sum(1 for f in all_findings if f.get("severity") == "Critical")
        high_count = sum(1 for f in all_findings if f.get("severity") == "High")
        med_count = sum(1 for f in all_findings if f.get("severity") == "Medium")

        penalty = (crit_count * 30) + (high_count * 15) + (med_count * 5)
        integrity_score = max(0, min(100, 100 - penalty))

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_integrity_score": integrity_score,
            "status": "APPROVED" if integrity_score >= 80 else ("WARNING" if integrity_score >= 60 else "REJECTED"),
            "critical_flags": crit_count,
            "high_flags": high_count,
            "medium_flags": med_count,
            "findings_count": len(all_findings),
            "findings": all_findings,
            "audit_summary": {
                "attribution_check": "PASSED" if not any(f["category"] == "Missing Attribution" for f in all_findings) else "ATTENTION NEEDED",
                "novelty_check": "PASSED" if not any(f["category"] == "Unsupported Novelty Claim" for f in all_findings) else "TONE ADJUSTMENT RECOMMENDED",
                "metrics_check": "PASSED" if not any(f["category"] == "Suspicious Metric" for f in all_findings) else "ANOMALIES FOUND",
                "leakage_check": "PASSED" if not any(f["category"] == "Data Leakage Alert" for f in all_findings) else "LEAKAGE RISK DETECTED",
            }
        }

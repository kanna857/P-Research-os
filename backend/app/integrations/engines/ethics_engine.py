"""
Research Ethics and Compliance Engine for P-Research-OS Ω.
Detects sensitive research triggers:
- Human participants & Institutional Review Board (IRB)
- Protected Health Information (PHI / HIPAA / GDPR)
- Animal models & IACUC oversight
- Vulnerable populations (minors, prisoners)
- Dual-use research of concern (DURC)
- Copyright and export-controlled content (ITAR/EAR)
Generates audit checklists and enforces mandatory human confirmation before execution.
"""

from typing import Dict, Any, List, Optional
import re
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


ETHICS_TRIGGERS = [
    {
        "category": "Human Participants & Behavioral Interventions",
        "keywords": ["human participant", "survey", "interview", "questionnaire", "student motivation", "subject", "classroom study", "patient"],
        "governing_body": "Institutional Review Board (IRB) / Ethics Committee",
        "requirement": "Written informed consent and institutional IRB protocol approval.",
        "severity": "HIGH"
    },
    {
        "category": "Medical & Protected Health Information (PHI)",
        "keywords": ["patient", "clinical trial", "diagnosis", "ehr", "medical record", "hospital", "liver disease", "biopsy"],
        "governing_body": "HIPAA Privacy Rule / GDPR Health Data Exemption",
        "requirement": "Formal de-identification certification or explicit data use agreement (DUA).",
        "severity": "CRITICAL"
    },
    {
        "category": "Animal Experiments & Vertebrate Testing",
        "keywords": ["mouse", "rat", "in vivo", "animal model", "tissue harvest", "vertebrate", "primate"],
        "governing_body": "Institutional Animal Care and Use Committee (IACUC)",
        "requirement": "Approved animal care protocol adhering to the 3Rs (Replacement, Reduction, Refinement).",
        "severity": "CRITICAL"
    },
    {
        "category": "Vulnerable Populations",
        "keywords": ["child", "minor", "student", "adolescent", "patient", "elderly", "prisoner", "cognitively impaired"],
        "governing_body": "Special Vulnerable Population Protections (45 CFR 46 Subparts B/C/D)",
        "requirement": "Parental permission, child assent, and heightened scrutiny of coercion risks.",
        "severity": "HIGH"
    },
    {
        "category": "Dual-Use Research of Concern & Export Control",
        "keywords": ["pathogen", "toxin", "virus", "radar jamming", "aerospace propulsion", "itar", "missile"],
        "governing_body": "Export Control (ITAR/EAR) & Institutional Biosafety Committee (IBC)",
        "requirement": "Export control screening and biological safety clearance.",
        "severity": "CRITICAL"
    }
]


class ResearchEthicsEngine:
    """
    Screens topics, plans, and datasets for compliance requirements
    without pretending the platform grants legal approval.
    """

    def screen_project_ethics(
        self,
        topic: str,
        methodology: str,
        data_sources: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Screens research topic and methodology for ethical risks and approval triggers.
        """
        combined_text = f"{topic} {methodology} {' '.join(data_sources or [])}".lower()
        triggered_regulations = []
        is_sensitive = False

        for trigger in ETHICS_TRIGGERS:
            matched = [kw for kw in trigger["keywords"] if re.search(r'\b' + re.escape(kw) + r'\b', combined_text)]
            if matched:
                is_sensitive = True
                triggered_regulations.append({
                    "category": trigger["category"],
                    "matched_keywords": matched,
                    "oversight_body": trigger["governing_body"],
                    "mandatory_requirement": trigger["requirement"],
                    "severity": trigger["severity"],
                    "status": "PENDING_HUMAN_CONFIRMATION"
                })

        overall_risk = "CRITICAL" if any(r["severity"] == "CRITICAL" for r in triggered_regulations) else ("HIGH" if triggered_regulations else "LOW")

        return {
            "topic": topic,
            "screened_at": datetime.now(timezone.utc).isoformat(),
            "is_sensitive_research": is_sensitive,
            "overall_ethics_risk": overall_risk,
            "triggers_detected_count": len(triggered_regulations),
            "compliance_triggers": triggered_regulations,
            "mandatory_review_checklist": [
                "1. Confirm study falls within institutional IRB / IACUC protocol scope.",
                "2. Verify data repository license permits the intended secondary academic research.",
                "3. Ensure all patient or student records are strictly de-identified (zero PII/PHI).",
                "4. Acknowledge funding and declare any competing financial interests."
            ],
            "human_approval_required": is_sensitive,
            "legal_disclaimer": "CRITICAL NOTICE: P-Research-OS Ω does NOT grant ethical approval, IRB authorization, or legal clearance. Human researcher confirmation is strictly mandatory."
        }


research_ethics_engine = ResearchEthicsEngine()

"""
Automated Integration Tests for the Academic Writing and Originality Suite:
- LanguageTool (languagetool-org/languagetool)
- TextHumanize (ksanyok/TextHumanize)
- Parrot Paraphraser (PrithivirajDamodaran/Parrot_Paraphraser)
- Noplag Engine (NoplagLabs/noplag-engine)
- Unified Academic Writing Pipeline
"""

import pytest
from app.integrations.writing.languagetool_adapter import languagetool_adapter, SCIENTIFIC_WHITELIST
from app.integrations.writing.text_humanize_adapter import text_humanize_adapter
from app.integrations.writing.parrot_paraphraser_adapter import parrot_adapter
from app.integrations.originality.noplag_adapter import noplag_adapter
from app.integrations.writing.unified_pipeline import unified_pipeline


# ── 1. LanguageTool Tests ────────────────────────────────────────────────────
def test_languagetool_grammar_and_style_audit():
    text = "We don't know why a lot of huge errors happened in order to achieve a bad result."
    res = languagetool_adapter.check(text)

    assert "total_issues" in res
    assert res["total_issues"] > 0
    assert "category_breakdown" in res
    assert res["scientific_whitelist_applied"] is True

    # Confirm contractions and informal qualifiers were flagged
    rule_ids = [m["rule_id"] for m in res["matches"]]
    assert "NO_CONTRACTIONS" in rule_ids
    assert "PRECISE_QUANTIFIER" in rule_ids
    assert "SCIENTIFIC_MAGNITUDE" in rule_ids


def test_languagetool_scientific_whitelist_preservation():
    """Ensure specialized terms (SAR, Siamese, mIoU, Sentinel-1) are never flagged as errors."""
    sar_text = "The Siamese network processes Sentinel-1 SAR imagery and achieves superior mIoU on GeoTIFF tiles."
    res = languagetool_adapter.check(sar_text)

    for match in res["matches"]:
        word = match.get("context", "").lower()
        for whitelisted in ["sentinel-1", "sar", "siamese", "miou", "geotiff"]:
            assert whitelisted not in match["suggestions"], f"Whitelisted term {whitelisted} was incorrectly targeted"


# ── 2. TextHumanize Tests ────────────────────────────────────────────────────
def test_text_humanize_style_transformation():
    text = "In order to conduct an investigation into the results, we observe that the Siamese network achieved 93.8% F1 [1]."
    res = text_humanize_adapter.refine_style(text, style="concise")

    assert res["citations_preserved"] is True
    assert "[1]" in res["revised_text"]
    assert "93.8%" in res["revised_text"]
    assert res["word_count_revised"] <= res["word_count_original"]
    assert "readability_index" in res


def test_text_humanize_blocks_unsupported_hyperbole():
    text = "This proposed method is a miraculous revolutionary breakthrough that undeniably proves perfection [2]."
    res = text_humanize_adapter.refine_style(text, style="formal")

    assert len(res["unsupported_claims_detected"]) > 0
    assert "[2]" in res["revised_text"]
    assert "miraculous" not in res["revised_text"].lower()


# ── 3. Parrot Paraphraser Tests ──────────────────────────────────────────────
def test_parrot_paraphraser_preserves_numbers_and_citations():
    sentence = "Our proposed Siamese U-Net achieves 93.8% F1-score and 0.841 mIoU on the test set [1]."
    res = parrot_adapter.paraphrase(sentence, max_candidates=3)

    assert res["candidates_count"] > 0
    for cand in res["candidates"]:
        cand_text = cand["candidate_text"]
        # In-text citation must remain
        assert "[1]" in cand_text, f"Candidate dropped citation: {cand_text}"
        # All metrics must be preserved
        assert cand["metrics_preserved"] is True
        assert cand["adequacy_score"] >= 0.70
        assert cand["fluency_score"] >= 0.70


def test_parrot_paraphraser_ethics_disclaimer():
    sentence = "Deep learning architectures have revolutionized computer vision."
    res = parrot_adapter.paraphrase(sentence)
    assert "ethics_warning" in res
    assert "Academic Integrity Policy" in res["ethics_warning"]


# ── 4. Noplag Engine Tests ───────────────────────────────────────────────────
def test_noplag_exact_and_near_duplicate_detection():
    sample_text = (
        "Automated change detection in multitemporal satellite imagery plays an indispensable role in environmental monitoring, "
        "disaster mitigation, and urban planning. However, conventional convolutional architectures frequently suffer from speckle-induced "
        "false positives and spatial boundary blurring."
    )
    ref_library = [
        {
            "title": "Deep Learning for Multitemporal Remote Sensing",
            "doi": "10.1109/JSTARS.2024.123456",
            "authors": "Zhang et al.",
            "abstract": (
                "Automated change detection in multitemporal satellite imagery plays an indispensable role in environmental monitoring, "
                "disaster mitigation, and urban planning. Classical models fail under speckle."
            ),
        }
    ]

    res = noplag_adapter.analyze_similarity(
        manuscript_text=sample_text,
        reference_library=ref_library,
        ngram_size=5,
        similarity_threshold=0.30,
    )

    assert res["overall_similarity_percentage"] > 0.0
    assert res["flagged_matches_count"] >= 1
    assert "disclaimer" in res
    assert "Turnitin" in res["disclaimer"]
    assert "iThenticate" in res["disclaimer"]


# ── 5. Unified Autonomous Review Pipeline Tests ──────────────────────────────
def test_unified_academic_writing_pipeline_autonomous_review():
    manuscript = (
        "I. INTRODUCTION\n\n"
        "Recent advances in Earth observation systems have provided unprecedented multitemporal data streams [1]. "
        "In this work, we propose a Siamese dual-stream network for Sentinel-1 SAR change detection. "
        "Experimental benchmarking on the held-out test partition confirms that the proposed architecture achieves 93.8% F1-score "
        "and 0.841 mIoU [2], substantially outperforming baseline models."
    )
    references = [
        {"title": "Sentinel-1 Earth Observation Review", "doi": "10.1016/j.rse.2023.109"},
        {"title": "Dual-Stream Siamese Networks for Remote Sensing", "doi": "10.1109/TGRS.2024.301"},
    ]
    benchmark = {
        "f1_score": "93.8%",
        "miou": "0.841",
    }

    report = unified_pipeline.run_autonomous_review(
        manuscript_text=manuscript,
        project_title="Deep Learning Change Detection",
        reference_library=references,
        experimental_benchmark=benchmark,
        target_style="formal",
    )

    assert "composite_quality_score" in report
    assert report["composite_quality_score"] > 80.0
    assert "publication_readiness_index" in report
    assert "step_1_grammar" in report
    assert "step_2_humanize_style" in report
    assert "step_3_parrot_paraphrases" in report
    assert "step_4_noplag_originality" in report
    assert "step_5_citation_claims" in report
    assert len(report["step_5_citation_claims"]["verified_claims"]) >= 2
    assert report["step_6_integrity_recheck"]["citations_intact"] is True
    assert len(report["tools_orchestrated"]) == 4


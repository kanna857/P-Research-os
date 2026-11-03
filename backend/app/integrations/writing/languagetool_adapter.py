"""
LanguageTool Integration Adapter (languagetool-org/languagetool).
Provides grammar, spelling, punctuation, and academic clarity verification,
with domain-specific whitelisting for scientific, remote sensing, and deep learning terms.
"""

from typing import List, Dict, Any, Optional, Set
import re


# Scientific terminology whitelist: these are NEVER flagged as spelling or grammar errors
SCIENTIFIC_WHITELIST: Set[str] = {
    # Remote Sensing & SAR
    "sar", "sentinel", "sentinel-1", "sentinel-2", "geotiff", "geotiffs", "backscatter",
    "radiometric", "polarimetric", "multitemporal", "interferometric", "insar", "copernicus",
    "subband", "swath", "azimuth", "polarization", "vv", "vh", "hh", "hv", "speckle",
    "co-registered", "coregistered", "multispectral", "orthorectified", "backscattering",
    # Computer Vision & Deep Learning
    "siamese", "resnet", "swin", "mobilenet", "mobilenetv3", "u-net", "unet", "miou", "iou",
    "f1-score", "dice", "transformer", "transformers", "attention", "cross-attention",
    "skip-connection", "skip-connections", "encoder-decoder", "backbone", "backbones",
    "featuremap", "featuremaps", "downsampling", "upsampling", "hyperparameter",
    "hyperparameters", "cross-entropy", "adamw", "optuna", "cleanlab", "fiftyone",
    "pytorch", "torchvision", "dvc", "grobid", "docling", "openalex", "unpaywall",
    # Mathematical & Evaluation
    "roc-auc", "auc", "roc", "confusion-matrix", "argmax", "softmax", "loss-function",
    "tpe", "bayesian", "shingling", "minhash", "jaccard", "cosine", "l1", "l2",
}


class LanguageToolAdapter:
    """
    Adapter for LanguageTool (languagetool-org/languagetool).
    Performs multi-category text auditing with scientific vocabulary protection.
    """

    def __init__(self):
        self._lt = None
        self._initialized = False

    def _get_engine(self):
        if not self._initialized:
            try:
                import language_tool_python
                self._lt = language_tool_python.LanguageTool("en-US")
            except Exception:
                self._lt = None
            self._initialized = True
        return self._lt

    def check(self, text: str) -> Dict[str, Any]:
        """
        Check text for grammar, spelling, punctuation, and academic style issues.
        Respects scientific terminology whitelist.
        """
        engine = self._get_engine()
        raw_issues = []

        # 1. If language_tool_python is available, query it
        if engine:
            try:
                matches = engine.check(text)
                for m in matches:
                    word = text[m.offset : m.offset + m.errorLength].lower()
                    if word in SCIENTIFIC_WHITELIST or re.sub(r"[^\w\-]", "", word) in SCIENTIFIC_WHITELIST:
                        continue
                    raw_issues.append({
                        "message": m.message,
                        "context": m.context,
                        "offset": m.offset,
                        "length": m.errorLength,
                        "rule_id": m.ruleId,
                        "category": self._categorize_rule(m.ruleId),
                        "suggestions": m.replacements[:4],
                    })
            except Exception:
                pass

        # 2. Comprehensive heuristic & academic style audit (applied alongside or as standalone)
        heuristic_issues = self._run_academic_heuristics(text)
        for hi in heuristic_issues:
            # Avoid duplicate offsets
            if not any(abs(r["offset"] - hi["offset"]) < 3 for r in raw_issues):
                raw_issues.append(hi)

        # Sort by offset
        raw_issues.sort(key=lambda x: x["offset"])

        # Statistics by category
        categories_count = {
            "GRAMMAR": 0,
            "SPELLING": 0,
            "PUNCTUATION": 0,
            "ACADEMIC_STYLE": 0,
            "SENTENCE_CLARITY": 0,
        }
        for iss in raw_issues:
            cat = iss.get("category", "GRAMMAR")
            if cat in categories_count:
                categories_count[cat] += 1
            else:
                categories_count["GRAMMAR"] += 1

        total_words = max(1, len(text.split()))
        quality_score = max(0, min(100, round(100 - (len(raw_issues) / total_words) * 150, 1)))

        return {
            "tool": "LanguageTool Professional Suite",
            "repository": "https://github.com/languagetool-org/languagetool",
            "total_issues": len(raw_issues),
            "quality_score": quality_score,
            "category_breakdown": categories_count,
            "matches": raw_issues,
            "scientific_whitelist_applied": True,
            "whitelist_terms_protected": len(SCIENTIFIC_WHITELIST),
        }

    def _categorize_rule(self, rule_id: str) -> str:
        rid = rule_id.upper()
        if any(k in rid for k in ["SPELL", "MORFOLOGIK", "TYPO"]):
            return "SPELLING"
        if any(k in rid for k in ["COMMA", "PUNCT", "PERIOD", "COLON", "SEMICOLON", "DASH", "QUOTE"]):
            return "PUNCTUATION"
        if any(k in rid for k in ["STYLE", "FORMAL", "COLLOQUIAL", "SLANG", "TONE"]):
            return "ACADEMIC_STYLE"
        if any(k in rid for k in ["CLARITY", "REDUNDAN", "WORDINESS", "LONG_SENTENCE"]):
            return "SENTENCE_CLARITY"
        return "GRAMMAR"

    def _run_academic_heuristics(self, text: str) -> List[Dict[str, Any]]:
        """Intelligent rule-based academic grammar, style, and consistency engine."""
        issues = []

        # Rules: (pattern, message, category, rule_id, suggestions)
        rules = [
            (
                r"\b(don't|can't|won't|isn't|aren't|didn't|doesn't|haven't|hasn't)\b",
                "Contracted verb forms should be avoided in formal academic manuscripts.",
                "ACADEMIC_STYLE",
                "NO_CONTRACTIONS",
                lambda m: [m.group(0).replace("n't", " not").replace("won't", "will not").replace("can't", "cannot")],
            ),
            (
                r"\b(a lot of|lots of)\b",
                "Informal quantifier detected. Prefer precise scholarly phrasing.",
                "ACADEMIC_STYLE",
                "PRECISE_QUANTIFIER",
                lambda m: ["numerous", "substantial", "a significant quantity of"],
            ),
            (
                r"\b(huge|massive|gigantic)\b",
                "Colloquial magnitude adjective. Use measured scientific terminology.",
                "ACADEMIC_STYLE",
                "SCIENTIFIC_MAGNITUDE",
                lambda m: ["substantial", "pronounced", "significant", "considerable"],
            ),
            (
                r"\b(good result|good results)\b",
                "Subjective qualifier. Use empirical evaluation phrasing.",
                "ACADEMIC_STYLE",
                "EMPIRICAL_PRECISION",
                lambda m: ["favorable outcome", "superior performance", "high empirical accuracy"],
            ),
            (
                r"\b(bad result|bad results)\b",
                "Informal evaluation qualifier. Use objective academic terminology.",
                "ACADEMIC_STYLE",
                "OBJECTIVE_EVALUATION",
                lambda m: ["suboptimal performance", "degraded accuracy", "inferior convergence"],
            ),
            (
                r"\b(etc\.|etc)\b",
                "'etc.' is discouraged in technical writing. Specify items or use 'among others'.",
                "ACADEMIC_STYLE",
                "AVOID_ETC",
                lambda m: ["among others", "and related parameters", "[itemized list]"],
            ),
            (
                r"\b(very unique|more unique)\b",
                "'Unique' is absolute and cannot be qualified by degree.",
                "GRAMMAR",
                "UNIQUE_ABSOLUTE",
                lambda m: ["unique", "distinctive", "novel"],
            ),
            (
                r"\b(irregardless)\b",
                "Non-standard term. Use 'regardless' or 'irrespective'.",
                "GRAMMAR",
                "STANDARD_ENGLISH",
                lambda m: ["regardless", "irrespective of"],
            ),
            (
                r"\b(in order to)\b",
                "Wordy construction. 'To' conveys the same meaning with higher conciseness.",
                "SENTENCE_CLARITY",
                "CONCISE_PURPOSE",
                lambda m: ["to"],
            ),
            (
                r"\b(due to the fact that)\b",
                "Redundant causal phrasing. Prefer 'because' or 'owing to'.",
                "SENTENCE_CLARITY",
                "CONCISE_CAUSALITY",
                lambda m: ["because", "since", "owing to"],
            ),
            (
                r"\s,([^\s])",
                "Spacing issue: space before comma or missing space after comma.",
                "PUNCTUATION",
                "COMMA_SPACING",
                lambda m: [f", {m.group(1)}"],
            ),
            (
                r"\b(their|there|they're)\b\s+(is|are)\s+no\b",
                "Check agreement and homophone consistency.",
                "GRAMMAR",
                "HOMOPHONE_CONSISTENCY",
                lambda m: ["there is no" if m.group(2) == "is" else "there are no"],
            ),
        ]

        for pattern, msg, cat, rule_id, sug_fn in rules:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                word = match.group(0)
                if word.lower() in SCIENTIFIC_WHITELIST:
                    continue
                start = match.start()
                end = match.end()
                context_start = max(0, start - 25)
                context_end = min(len(text), end + 25)
                context = text[context_start:context_end]
                suggestions = sug_fn(match)
                issues.append({
                    "message": msg,
                    "context": context,
                    "offset": start,
                    "length": end - start,
                    "rule_id": rule_id,
                    "category": cat,
                    "suggestions": suggestions,
                })

        return issues


languagetool_adapter = LanguageToolAdapter()


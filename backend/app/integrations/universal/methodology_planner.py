"""
Universal Research Methodology Planner for P-Research-OS Ω.
Selects scientifically appropriate research methodologies across:
- Computational research
- Experimental research
- Observational research
- Theoretical research
- Simulation research
- Qualitative research
- Systematic reviews
- Meta-analysis
- Mixed-methods research
Generates 10-point comprehensive methodology plans with human-in-the-loop approval checkpoints.
"""

from typing import Dict, Any, List, Optional
import re
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


# Supported Universal Methodologies
METHODOLOGIES: Dict[str, Dict[str, Any]] = {
    "computational": {
        "label": "Computational Research",
        "description": "Algorithm development, software benchmarking, machine learning, and empirical computational experiments.",
        "analysis_methods": ["Cross-validation (k-fold / spatial)", "Ablation studies", "Performance profiling", "Confusion matrix & ROC analysis"],
        "evaluation_criteria": ["F1-Score / Accuracy / IoU", "Execution latency / FLOPs", "Convergence rate", "Reproducibility on held-out test splits"],
        "requires_physical_lab": False,
        "requires_irb": False,
    },
    "experimental": {
        "label": "Experimental Research",
        "description": "Controlled laboratory interventions, measurement protocols, instrument readings, and physical specimen assays.",
        "analysis_methods": ["Controlled variable comparison", "Standardized assay protocol", "Instrument calibration checks", "Factorial ANOVA"],
        "evaluation_criteria": ["Measurement precision & error bounds", "Assay reproducibility", "Inter-instrument variance", "Signal-to-noise ratio"],
        "requires_physical_lab": True,
        "requires_irb": False,  # May require IACUC if animal
    },
    "observational": {
        "label": "Observational & Epidemiological Research",
        "description": "Surveys, longitudinal cohorts, cross-sectional records, observational registries, and econometric time-series.",
        "analysis_methods": ["Multivariate regression", "Propensity score matching", "Time-series decomposition (ARIMA/VAR)", "Survival analysis (Kaplan-Meier)"],
        "evaluation_criteria": ["Statistical significance (p < 0.05, 95% CI)", "R-squared / Adjusted R-squared", "Confounding bias control", "External validity"],
        "requires_physical_lab": False,
        "requires_irb": True,
    },
    "theoretical": {
        "label": "Theoretical & Formal Research",
        "description": "Mathematical modeling, formal reasoning, symbolic derivations, theorem proving, and conceptual frameworks.",
        "analysis_methods": ["Symbolic calculus & differentiation", "Axiomatic proof deduction", "Asymptotic complexity analysis", "Analytical closed-form derivation"],
        "evaluation_criteria": ["Mathematical soundness", "Absence of contradictory assumptions", "Generality of theorems", "Verification via computer algebra (SymPy)"],
        "requires_physical_lab": False,
        "requires_irb": False,
    },
    "simulation": {
        "label": "Simulation & Numerical Research",
        "description": "Physics simulations, differential equation numerical solvers (ODE/PDE), finite element modeling, and Monte Carlo experiments.",
        "analysis_methods": ["Runge-Kutta numerical integration", "Finite element mesh discretization", "Monte Carlo stochastic sampling", "Sensitivity & parameter sweeps"],
        "evaluation_criteria": ["Mesh convergence & conservation of energy/mass", "Numerical stability (CFL condition)", "Residual error tolerances", "Comparison with analytical benchmarks"],
        "requires_physical_lab": False,
        "requires_irb": False,
    },
    "qualitative": {
        "label": "Qualitative Research",
        "description": "Thematic analysis, semi-structured interviews, document analysis, grounded theory, and qualitative synthesis.",
        "analysis_methods": ["Inductive / deductive thematic coding", "Codebook consensus development", "Constant comparative method", "Discourse analysis"],
        "evaluation_criteria": ["Inter-coder agreement (Cohen's Kappa)", "Theoretical saturation", "Audit trail credibility", "Member checking"],
        "requires_physical_lab": False,
        "requires_irb": True,
    },
    "systematic_review": {
        "label": "Systematic Review (PRISMA)",
        "description": "Structured protocol-driven literature search, transparent inclusion/exclusion screening, quality assessment, and evidence synthesis.",
        "analysis_methods": ["PRISMA 2020 4-phase flow screening", "Risk of bias assessment (Cochrane RoB / ROBINS-I)", "Structured data extraction forms", "Thematic evidence synthesis"],
        "evaluation_criteria": ["Comprehensive search coverage (3+ databases)", "Dual-reviewer screening agreement", "Transparent exclusion logging", "Methodological quality grading"],
        "requires_physical_lab": False,
        "requires_irb": False,
    },
    "meta_analysis": {
        "label": "Meta-Analysis & Statistical Pooling",
        "description": "Quantitative synthesis of effect sizes across independent studies, heterogeneity assessment, and publication-bias auditing.",
        "analysis_methods": ["Hedges' g / Cohen's d effect size extraction", "Random-effects / fixed-effects pooling", "Cochran's Q and I-squared heterogeneity testing", "Funnel plot Egger's test for publication bias"],
        "evaluation_criteria": ["Pooled effect size confidence intervals", "Heterogeneity quantification (I-squared < 50%)", "Subgroup and sensitivity robustness", "Absence of funnel plot asymmetry"],
        "requires_physical_lab": False,
        "requires_irb": False,
    },
    "mixed_methods": {
        "label": "Mixed-Methods Research",
        "description": "Convergent or sequential integration of quantitative statistical measurements with in-depth qualitative evidence.",
        "analysis_methods": ["Joint display analysis", "Convergent parallel data triangulation", "Sequential explanatory design", "Integrated qualitative-quantitative matrices"],
        "evaluation_criteria": ["Triangulation consistency", "Complementarity of qualitative depth and quantitative breadth", "Explicit integration justification"],
        "requires_physical_lab": False,
        "requires_irb": True,
    }
}


class UniversalMethodologyPlanner:
    """
    Plans discipline-appropriate research protocols, formulates hypotheses,
    and establishes scientific evaluation criteria without forcing ML pipelines.
    """

    def plan_methodology(
        self,
        topic: str,
        domain_routing: Dict[str, Any],
        user_methodology_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive 10-point scientific methodology plan tailored
        to the topic and domain characteristics.
        """
        primary_domain = domain_routing.get("primary_domain", "Interdisciplinary Research")
        default_method = domain_routing.get("default_methodology", "computational")

        # Select methodology: user override > inferred domain default > keyword heuristics
        selected_method_key = self._resolve_methodology(topic, default_method, user_methodology_override)
        method_meta = METHODOLOGIES.get(selected_method_key, METHODOLOGIES["computational"])

        # Formulate research questions
        research_questions = self._formulate_research_questions(topic, primary_domain, selected_method_key)

        # Formulate hypothesis (if applicable)
        hypothesis = self._formulate_hypothesis(topic, selected_method_key)

        # Establish 10-point plan
        plan = {
            "topic": topic,
            "primary_domain": primary_domain,
            "selected_methodology_key": selected_method_key,
            "methodology_name": method_meta["label"],
            "methodology_description": method_meta["description"],
            "plan_generated_at": datetime.now(timezone.utc).isoformat(),

            # 1. Research Objective
            "1_research_objective": f"To rigorously investigate, evaluate, and provide evidence-grounded findings for: '{topic}', applying established {method_meta['label']} standards in {primary_domain}.",

            # 2. Research Questions
            "2_research_questions": research_questions,

            # 3. Hypotheses
            "3_hypotheses": hypothesis,

            # 4. Study Design
            "4_study_design": self._generate_study_design(topic, selected_method_key, primary_domain),

            # 5. Data Requirements
            "5_data_requirements": {
                "evidence_sources": domain_routing.get("evidence_requirements", ["Peer-reviewed literature"]),
                "dataset_requirements": domain_routing.get("dataset_requirements", ["Benchmark records"]),
                "provenance_policy": "Strict DOI and repository tracking with zero simulated data presented as real."
            },

            # 6. Analysis Methods
            "6_analysis_methods": method_meta["analysis_methods"],

            # 7. Evaluation Criteria
            "7_evaluation_criteria": method_meta["evaluation_criteria"],

            # 8. Risks and Scientific Limitations
            "8_risks_and_limitations": [
                f"Methodological constraint: Findings are bounded by the assumptions of {method_meta['label']}.",
                "Sampling & Generalizability: Results apply strictly to validated datasets/parameters within study scope.",
                "Non-Execution Disclaimer: No physical lab experiments or human subject interventions are claimed unless certified by human evidence."
            ],

            # 9. Reproducibility Requirements
            "9_reproducibility_requirements": [
                "Full reproducibility manifest (reproducibility_manifest.json) recording code, dependencies, and seeds.",
                "Open dataset access or standardized public repository identifier (DOI / accession).",
                "Computational environment frozen (pip requirements.txt / Conda environment.yml)."
            ],

            # 10. Human Approval Requirements
            "10_human_approval_requirements": {
                "requires_human_checkpoint": True,
                "requires_physical_lab_confirmation": method_meta["requires_physical_lab"],
                "requires_irb_ethics_confirmation": method_meta["requires_irb"],
                "approval_checkpoints": [
                    "Topic Scope Confirmation",
                    "Methodology Suitability Verification",
                    "Dataset License & Provenance Verification",
                    "Statistical Assumption Validation",
                    "Final Manuscript Publication Sign-off"
                ]
            }
        }

        return plan

    def _resolve_methodology(self, topic: str, default_method: str, override: Optional[str]) -> str:
        """Determines best-fitting methodology key."""
        if override and override.lower() in METHODOLOGIES:
            return override.lower()

        lower = topic.lower()

        # Keyword heuristics
        if any(w in lower for w in ["systematic review", "meta-analysis", "meta analysis", "literature review", "scoping review"]):
            return "systematic_review" if "meta" not in lower else "meta_analysis"
        if any(w in lower for w in ["numerical simulation", "heat transfer", "finite element", "cfd", "monte carlo simulation", "aerodynamic simulation"]):
            return "simulation"
        if any(w in lower for w in ["symbolic", "differential equations", "theorem", "proof", "analytical solution", "formal analysis"]):
            return "theoretical"
        if any(w in lower for w in ["qualitative", "interview", "thematic analysis", "ethnograph", "case study", "grounded theory"]):
            return "qualitative"
        if any(w in lower for w in ["survey", "epidemiological", "cohort", "longitudinal", "forecasting", "inflation", "econometric", "time-series"]):
            return "observational"
        if any(w in lower for w in ["laboratory experiment", "synthesis", "assay", "in vitro", "controlled trial"]):
            return "experimental"
        if any(w in lower for w in ["deep learning", "neural network", "machine learning", "change detection", "classification", "segmentation", "sar", "algorithm"]):
            return "computational"

        return default_method if default_method in METHODOLOGIES else "computational"

    def _formulate_research_questions(self, topic: str, domain: str, method: str) -> List[str]:
        """Generates 3 focused, discipline-appropriate research questions."""
        if method == "systematic_review":
            return [
                f"RQ1: What is the current state of empirical evidence regarding {topic} across peer-reviewed literature?",
                f"RQ2: What methodological approaches and intervention designs predominate in current studies?",
                f"RQ3: What consistent outcome effects, risk-of-bias factors, and research gaps characterize the field?"
            ]
        elif method == "simulation":
            return [
                f"RQ1: How do governing physical parameters influence system dynamics in {topic} under varying boundary conditions?",
                f"RQ2: What is the convergence behavior and numerical stability of the proposed discretization solver?",
                f"RQ3: How closely do simulated results correlate with established analytical reference solutions?"
            ]
        elif method == "theoretical":
            return [
                f"RQ1: Can formal closed-form solutions or asymptotic bounds be derived for the governing formulations of {topic}?",
                f"RQ2: Under what parameter manifolds and initial conditions do stable equilibrium states exist?",
                f"RQ3: How do symbolic derivations compare against verified numerical approximations?"
            ]
        elif method == "observational":
            return [
                f"RQ1: What statistically significant relationships exist within observational datasets for {topic}?",
                f"RQ2: How robust are predictive models when controlling for confounding covariates and temporal autocorrelation?",
                f"RQ3: To what extent do out-of-sample forecasts maintain precision across independent time horizons?"
            ]
        elif method == "qualitative":
            return [
                f"RQ1: How do participants and primary documents conceptualize the core dimensions of {topic}?",
                f"RQ2: What emergent themes and contextual patterns characterize participant experiences?",
                f"RQ3: How do qualitative findings inform or challenge prevailing theoretical models in {domain}?"
            ]
        else:  # computational / default
            return [
                f"RQ1: How does the proposed computational framework perform on benchmark datasets for {topic} compared to standard baselines?",
                f"RQ2: What is the quantitative contribution of individual architectural components in ablation tests?",
                f"RQ3: How robust is the model against noise, domain shifts, and data sparsity?"
            ]

    def _formulate_hypothesis(self, topic: str, method: str) -> Optional[Dict[str, str]]:
        """Formulates testable scientific hypothesis where appropriate."""
        if method in ("theoretical", "qualitative", "systematic_review"):
            return None  # Exploratory / inductive research designs do not require a priori null hypotheses

        return {
            "null_hypothesis_H0": f"The proposed method or intervention produces no statistically significant difference in outcome metrics for '{topic}' compared to baseline controls (delta = 0).",
            "alternative_hypothesis_H1": f"The proposed approach produces a statistically significant improvement or variation in outcome metrics for '{topic}' with p < 0.05 and verified effect size."
        }

    def _generate_study_design(self, topic: str, method: str, domain: str) -> Dict[str, Any]:
        """Provides concrete protocol details for the selected study design."""
        designs = {
            "computational": {
                "design_type": "Empirical Benchmark & Ablation Study",
                "sampling_protocol": "80/20 non-overlapping train/test partition with isolated cross-validation",
                "control_conditions": "Baseline architectures and ablation with stripped attention heads",
                "instrumentation": "PyTorch / GPU acceleration with deterministic random seeds"
            },
            "experimental": {
                "design_type": "Controlled Laboratory Protocol",
                "sampling_protocol": "Standardized specimen sampling with replicate measurements (n >= 3)",
                "control_conditions": "Negative control, vehicle control, and positive reference standards",
                "instrumentation": "Calibrated analytical instruments with recorded serial numbers"
            },
            "observational": {
                "design_type": "Retrospective Cohort & Time-Series Econometric Design",
                "sampling_protocol": "Multi-period temporal sampling with stationary unit-root validation",
                "control_conditions": "Controlling for demographic covariates and macroeconomic confounders",
                "instrumentation": "Standardized registry databases (FRED, OECD, IPUMS, ClinicalTrials)"
            },
            "theoretical": {
                "design_type": "Axiomatic Formulation & Symbolic Derivation",
                "sampling_protocol": "Comprehensive parameter phase space exploration",
                "control_conditions": "Limiting cases corresponding to known classical solutions",
                "instrumentation": "Computer algebra systems (SymPy) with numerical validation grids"
            },
            "simulation": {
                "design_type": "Numerical Continuum / Monte Carlo Simulation Design",
                "sampling_protocol": "Multi-scale grid refinement with spatial/temporal convergence tests",
                "control_conditions": "Boundary condition sensitivity sweeps and analytical benchmark comparison",
                "instrumentation": "Scientific ODE/PDE solvers (SciPy / FEniCS / OpenFOAM)"
            },
            "qualitative": {
                "design_type": "Inductive / Deductive Thematic Analysis",
                "sampling_protocol": "Purposive criterion sampling until theoretical saturation",
                "control_conditions": "Triangulation across documents, interviews, and field notes",
                "instrumentation": "Qualitative codebook with dual-coder consensus verification"
            },
            "systematic_review": {
                "design_type": "PRISMA 2020 Systematic Evidence Synthesis",
                "sampling_protocol": "Comprehensive bibliographic search across 3+ academic repositories",
                "control_conditions": "Strict inclusion/exclusion criteria applied independently by dual reviewers",
                "instrumentation": "Standardized Cochrane Risk of Bias / ROBINS-I appraisal instruments"
            },
            "meta_analysis": {
                "design_type": "Quantitative Effect Size Pooling & Meta-Regression",
                "sampling_protocol": "Exhaustive extraction of standardized mean differences or odds ratios",
                "control_conditions": "Random-effects vs fixed-effects weighting and sensitivity jackknifing",
                "instrumentation": "Forest plots, funnel plots, and I-squared heterogeneity statistics"
            },
            "mixed_methods": {
                "design_type": "Convergent Parallel Mixed-Methods Integration",
                "sampling_protocol": "Concurrent collection of quantitative surveys and in-depth qualitative cases",
                "control_conditions": "Side-by-side joint display comparison of statistical and thematic findings",
                "instrumentation": "Triangulation matrices validating convergence or divergence"
            }
        }
        return designs.get(method, designs["computational"])


universal_methodology_planner = UniversalMethodologyPlanner()

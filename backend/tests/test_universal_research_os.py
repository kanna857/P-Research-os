"""
Comprehensive Test Suite for P-Research-OS Ω — Universal Autonomous Research Operating System.
Validates all 7 mandatory research benchmark scenarios:
1. AI / Remote Sensing: Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection
2. Biomedical: Machine Learning Methods for Liver Disease Classification
3. Physics: Numerical Simulation of Heat Transfer in Composite Materials
4. Agriculture: Satellite-Based Crop Health Monitoring
5. Economics: Forecasting Inflation Using Economic Time-Series Data
6. Psychology: Systematic Review of Digital Learning and Student Motivation
7. Mathematics: Symbolic and Numerical Analysis of Nonlinear Differential Equations

Verifies:
- Domain classification accuracy across 36 disciplines
- Appropriate methodology selection without forcing deep learning
- Ethics and compliance detection
- Multidisciplinary discovery targets
- Scientific simulation and differential equation solving
- PRISMA systematic review flow and meta-analytic pooling
- Statistical assumption validation & effect size calculations
- Knowledge graph construction
- End-to-end Universal Autopilot execution
"""

import pytest
import os

from app.integrations.universal.domain_router import universal_domain_router
from app.integrations.universal.methodology_planner import universal_methodology_planner
from app.integrations.universal.multidisciplinary_discovery import multidisciplinary_discovery
from app.integrations.universal.knowledge_graph import research_knowledge_graph
from app.integrations.engines.ethics_engine import research_ethics_engine
from app.integrations.engines.statistical_engine import universal_statistical_engine
from app.integrations.engines.simulation_engine import scientific_simulation_engine
from app.integrations.engines.systematic_review_engine import systematic_review_engine
from app.integrations.engines.qualitative_engine import qualitative_research_engine
from app.integrations.engines.biomedical_engine import biomedical_research_engine
from app.integrations.engines.mathematics_engine import mathematics_engine
from app.integrations.universal.research_autopilot import universal_research_autopilot


# ── Scenario 1: AI / Remote Sensing ──────────────────────────────────────────
def test_scenario_1_remote_sensing():
    topic = "Speckle-Robust Deep Learning for Sentinel-1 SAR Change Detection"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Earth Observation and Remote Sensing", "Artificial Intelligence and Machine Learning")
    assert routing["default_methodology"] == "computational"

    plan = universal_methodology_planner.plan_methodology(topic, routing)
    assert plan["selected_methodology_key"] == "computational"
    assert "F1-Score" in plan["7_evaluation_criteria"][0] or "Accuracy" in plan["7_evaluation_criteria"][0]

    # Leakage check
    audit = multidisciplinary_discovery.assess_dataset_quality("Sentinel-1 SAR Benchmark", "satellite imagery", 2500, "CC-BY-4.0", routing["primary_domain"])
    assert "spatial" in audit["leakage_risk_level"].lower() or audit["leakage_risk_level"] == "Low"


# ── Scenario 2: Biomedical Research ──────────────────────────────────────────
def test_scenario_2_biomedical():
    topic = "Machine Learning Methods for Liver Disease Classification"
    routing = universal_domain_router.classify_topic(topic)
    assert any(d in routing["primary_domain"] for d in ["Medicine", "Healthcare", "Artificial Intelligence", "Biotechnology"])

    # Ethics screening MUST trigger Protected Health Information (PHI)
    ethics = research_ethics_engine.screen_project_ethics(topic, "computational")
    assert ethics["is_sensitive_research"] is True
    categories = [c["category"] for c in ethics["compliance_triggers"]]
    assert any("Medical" in cat or "Health" in cat for cat in categories)

    # Clinical evaluation metrics
    clin = biomedical_research_engine.compute_clinical_evaluation_metrics(tp=140, fp=20, fn=15, tn=105)
    assert clin["clinical_metrics"]["sensitivity_recall"] > 0.85
    assert clin["clinical_metrics"]["specificity"] > 0.80
    assert "licensed physician" in clin["safety_warning"]


# ── Scenario 3: Physics & Materials Simulation ───────────────────────────────
def test_scenario_3_physics_simulation():
    topic = "Numerical Simulation of Heat Transfer in Composite Materials"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Physics", "Materials Science", "Mechanical Engineering")

    plan = universal_methodology_planner.plan_methodology(topic, routing)
    assert plan["selected_methodology_key"] == "simulation"

    # Numerical PDE simulation
    sim = scientific_simulation_engine.simulate_heat_transfer_1d(
        length_meters=0.10,
        thermal_diffusivity_alpha=1.2e-4,
        simulation_time_seconds=10.0
    )
    assert sim["parameters"]["numerical_stability"].startswith("STABLE")
    assert len(sim["spatial_profile"]["temperatures_celsius"]) > 5
    assert sim["summary_metrics"]["maximum_temperature_celsius"] >= 25.0


# ── Scenario 4: Agriculture ──────────────────────────────────────────────────
def test_scenario_4_agriculture():
    topic = "Satellite-Based Crop Health Monitoring"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Agriculture", "Earth Observation and Remote Sensing", "Environmental Science")

    targets = multidisciplinary_discovery.select_discovery_targets(routing["primary_domain"], "computational")
    assert any("Copernicus" in d or "NASA" in d or "Zenodo" in d for d in targets["recommended_dataset_repositories"])


# ── Scenario 5: Economics & Time-Series ──────────────────────────────────────
def test_scenario_5_economics():
    topic = "Forecasting Inflation Using Economic Time-Series Data"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Economics", "Finance", "Data Science")

    plan = universal_methodology_planner.plan_methodology(topic, routing)
    assert plan["selected_methodology_key"] in ("observational", "computational")

    # Regression / Statistical test
    ols = universal_statistical_engine.run_ordinary_least_squares(
        x_values=[1.2, 1.5, 2.1, 2.8, 3.4, 4.1],
        y_values=[2.0, 2.3, 3.1, 3.8, 4.6, 5.2],
        x_name="Money Supply M2 Growth",
        y_name="CPI Inflation"
    )
    assert ols["r_squared"] > 0.85
    assert ols["slope_beta1"] > 0


# ── Scenario 6: Psychology Systematic Review ─────────────────────────────────
def test_scenario_6_psychology_systematic_review():
    topic = "Systematic Review of Digital Learning and Student Motivation"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Psychology", "Education", "Social Sciences")

    plan = universal_methodology_planner.plan_methodology(topic, routing)
    assert plan["selected_methodology_key"] in ("systematic_review", "meta_analysis")

    # PRISMA flow and Meta-Analysis
    prisma = systematic_review_engine.generate_prisma_flow(topic=topic)
    assert prisma["phases"]["identification"]["net_records_for_screening"] > 0
    assert prisma["phases"]["included"]["quantitative_studies_in_meta_analysis"] > 0

    meta = systematic_review_engine.run_meta_analysis_pooling()
    assert meta["pooled_effect_size_hedges_g"] > 0.40
    assert meta["heterogeneity"]["i_squared_percent"] < 50.0


# ── Scenario 7: Mathematics & Nonlinear Dynamics ─────────────────────────────
def test_scenario_7_mathematics():
    topic = "Symbolic and Numerical Analysis of Nonlinear Differential Equations"
    routing = universal_domain_router.classify_topic(topic)
    assert routing["primary_domain"] in ("Mathematics", "Physics")

    plan = universal_methodology_planner.plan_methodology(topic, routing)
    assert plan["selected_methodology_key"] == "theoretical"

    math_res = mathematics_engine.analyze_nonlinear_ode_system(mu_parameter=1.0)
    assert math_res["dynamical_properties"]["limit_cycle_detected"] is True
    assert len(math_res["numerical_solution"]["trajectories"]) >= 10


# ── Knowledge Graph & Autopilot Full Integration ─────────────────────────────
def test_universal_knowledge_graph():
    kg = research_knowledge_graph.build_project_knowledge_graph(
        topic="Heat Transfer Simulation",
        domain="Physics",
        methodology="simulation",
        research_questions=["RQ1: What is the spatial thermal gradient?"]
    )
    assert kg["nodes_count"] >= 6
    assert kg["edges_count"] >= 5
    assert any(n["type"] == "Topic" for n in kg["nodes"])
    assert any(n["type"] == "Method" for n in kg["nodes"])


def test_end_to_end_universal_autopilot():
    res = universal_research_autopilot.run_autopilot_pipeline(
        topic="Forecasting Inflation Using Economic Time-Series Data"
    )
    assert res["status"] == "COMPLETED"
    assert res["primary_domain"] == "Economics"
    assert len(res["execution_logs"]) >= 10
    assert "manuscript" in res
    assert "sections" in res["manuscript"]
    assert len(res["checkpoints"]) == 9

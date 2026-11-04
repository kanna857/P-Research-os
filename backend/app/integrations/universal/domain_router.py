"""
Universal Research Domain Router for P-Research-OS Ω.
Taxonomy-driven and semantic classification across 36 academic disciplines.
Identifies primary and secondary domains, confidence, subfields, query expansions,
required evidence types, dataset needs, and ethical/regulatory considerations.
"""

from typing import Dict, Any, List, Optional
import re
import math
import logging
from datetime import datetime, timezone

from app.integrations.nhost.semantic_search import SemanticSearchEngine

logger = logging.getLogger(__name__)


# Universal Taxonomy of 36 Academic and Scientific Disciplines
RESEARCH_DOMAINS: Dict[str, Dict[str, Any]] = {
    # ── Computational & Formal Sciences ──────────────────────────────────────
    "Artificial Intelligence and Machine Learning": {
        "category": "Formal & Computing",
        "keywords": ["machine learning", "deep learning", "neural network", "transformer", "reinforcement learning", "computer vision", "nlp", "llm", "classification", "clustering"],
        "default_methodology": "computational",
        "evidence_types": ["benchmark datasets", "empirical metrics", "open-source code", "ablation studies"],
        "data_requirements": ["curated training/validation/test splits", "ground-truth annotations"],
        "computational_needs": "GPU acceleration / PyTorch / CUDA",
        "ethical_considerations": ["algorithmic bias", "fairness", "model transparency", "energy footprint"]
    },
    "Computer Science": {
        "category": "Formal & Computing",
        "keywords": ["algorithms", "distributed systems", "operating system", "software engineering", "compiler", "database system", "cloud computing", "networking"],
        "default_methodology": "computational",
        "evidence_types": ["system benchmarks", "complexity proofs", "execution latency logs", "code artifacts"],
        "data_requirements": ["workload traces", "synthetic test suites"],
        "computational_needs": "Multi-core CPU / networked cluster",
        "ethical_considerations": ["software security", "intellectual property", "open-source licensing"]
    },
    "Cybersecurity": {
        "category": "Formal & Computing",
        "keywords": ["cryptography", "malware", "vulnerability", "intrusion detection", "penetration testing", "zero trust", "network security", "exploit"],
        "default_methodology": "computational",
        "evidence_types": ["attack logs", "vulnerability datasets", "formal protocol verifications"],
        "data_requirements": ["anonymized traffic traces", "CVE databases", "sandbox execution telemetry"],
        "computational_needs": "Isolated sandbox / virtualization",
        "ethical_considerations": ["dual-use risk", "responsible disclosure", "user privacy", "unauthorized testing"]
    },
    "Data Science": {
        "category": "Formal & Computing",
        "keywords": ["data mining", "exploratory data analysis", "predictive modeling", "big data", "feature engineering", "data visualization", "pandas"],
        "default_methodology": "computational",
        "evidence_types": ["tabular datasets", "statistical significance tests", "validation metrics"],
        "data_requirements": ["structured / semi-structured records", "data dictionaries"],
        "computational_needs": "High-memory computing / distributed analytics",
        "ethical_considerations": ["data anonymization", "consent", "sampling bias"]
    },
    "Mathematics": {
        "category": "Formal & Computing",
        "keywords": ["differential equations", "topology", "linear algebra", "discrete mathematics", "probability theory", "real analysis", "symbolic", "proof", "nonlinear"],
        "default_methodology": "theoretical",
        "evidence_types": ["formal mathematical proofs", "symbolic derivations", "numerical verification"],
        "data_requirements": ["initial/boundary conditions", "analytical closed forms"],
        "computational_needs": "Symbolic computer algebra (SymPy / SageMath)",
        "ethical_considerations": ["scientific rigor", "reproducible analytical derivations"]
    },

    # ── Physical & Engineering Sciences ──────────────────────────────────────
    "Physics": {
        "category": "Physical Sciences",
        "keywords": ["quantum", "thermodynamics", "heat transfer", "fluid dynamics", "particle physics", "optics", "electromagnetism", "astrophysics", "composite materials"],
        "default_methodology": "simulation",
        "evidence_types": ["numerical simulation logs", "governing differential equations", "experimental telemetry"],
        "data_requirements": ["material properties", "boundary conditions", "sensor measurements"],
        "computational_needs": "Scientific numerical libraries (NumPy / SciPy / OpenFOAM / FEniCS)",
        "ethical_considerations": ["distinction between simulation vs physical measurement", "dual-use technology"]
    },
    "Chemistry": {
        "category": "Physical Sciences",
        "keywords": ["molecular", "chemical reaction", "catalysis", "organic chemistry", "inorganic chemistry", "spectroscopy", "synthesis", "cheminformatics", "rdkit"],
        "default_methodology": "computational",
        "evidence_types": ["SMILES strings", "crystallographic structures", "spectroscopic data", "reaction pathways"],
        "data_requirements": ["PubChem / ChEMBL databases", "molecular conformations"],
        "computational_needs": "RDKit / ASE / DFT simulation suites",
        "ethical_considerations": ["hazardous materials safety", "chemical security", "lab verification required"]
    },
    "Materials Science": {
        "category": "Physical Sciences",
        "keywords": ["composite materials", "nanomaterials", "polymers", "metallurgy", "tensile strength", "crystal structure", "bandgap", "thermal conductivity"],
        "default_methodology": "simulation",
        "evidence_types": ["stress-strain curves", "microscopy images", "finite element analysis"],
        "data_requirements": ["materials project entries", "mechanical property tables"],
        "computational_needs": "Pymatgen / Finite Element Modeling",
        "ethical_considerations": ["environmental life cycle", "toxicity of nanoparticles"]
    },
    "Electrical Engineering": {
        "category": "Engineering",
        "keywords": ["signal processing", "power systems", "circuits", "vlsi", "telecommunications", "antenna", "semiconductor", "fpga"],
        "default_methodology": "simulation",
        "evidence_types": ["SPICE simulations", "waveform captures", "frequency response curves"],
        "data_requirements": ["circuit netlists", "RF spectra"],
        "computational_needs": "Simulation software / digital signal processors",
        "ethical_considerations": ["electromagnetic safety", "grid stability", "e-waste"]
    },
    "Electronics": {
        "category": "Engineering",
        "keywords": ["microelectronics", "integrated circuits", "pcb design", "sensors", "embedded systems", "microcontroller", "iot"],
        "default_methodology": "experimental",
        "evidence_types": ["schematics", "oscilloscope logs", "timing diagrams"],
        "data_requirements": ["sensor telemetry", "component datasheets"],
        "computational_needs": "CAD tools / firmware toolchains",
        "ethical_considerations": ["hardware trojans", "component provenance"]
    },
    "Mechanical Engineering": {
        "category": "Engineering",
        "keywords": ["thermodynamics", "finite element", "cad", "solid mechanics", "heat transfer", "turbomachinery", "aerodynamics", "kinematics"],
        "default_methodology": "simulation",
        "evidence_types": ["CAD geometries", "mesh convergence graphs", "thermal dissipation maps"],
        "data_requirements": ["boundary loads", "thermal conductivity coefficients"],
        "computational_needs": "Finite element solvers / CAD mesh generators",
        "ethical_considerations": ["structural safety margins", "failure risk assessments"]
    },
    "Civil Engineering": {
        "category": "Engineering",
        "keywords": ["structural analysis", "concrete", "geotechnical", "hydrology", "transportation network", "earthquake engineering", "bridge", "urban infrastructure"],
        "default_methodology": "simulation",
        "evidence_types": ["soil bore logs", "stress contours", "traffic flow statistics"],
        "data_requirements": ["GIS terrain maps", "seismic accelerometer logs"],
        "computational_needs": "Geotechnical and structural modeling software",
        "ethical_considerations": ["public safety", "environmental impact assessment", "building codes"]
    },
    "Robotics": {
        "category": "Engineering",
        "keywords": ["kinematics", "slam", "autonomous mobile robots", "actuators", "ros", "manipulators", "path planning", "motion control"],
        "default_methodology": "simulation",
        "evidence_types": ["trajectory tracking curves", "state estimation errors", "simulation logs"],
        "data_requirements": ["LiDAR point clouds", "odometry feeds", "URDF model definitions"],
        "computational_needs": "Physics engines (PyBullet / Gazebo)",
        "ethical_considerations": ["human-robot interaction safety", "autonomous liability", "physical hazard prevention"]
    },
    "Aerospace Engineering": {
        "category": "Engineering",
        "keywords": ["aerodynamics", "orbital mechanics", "propulsion", "avionics", "spacecraft", "uav", "thrust", "computational fluid dynamics"],
        "default_methodology": "simulation",
        "evidence_types": ["CFD lift/drag polar curves", "trajectory simulations", "telemetry"],
        "data_requirements": ["atmospheric profiles", "engine test bench data"],
        "computational_needs": "High-fidelity CFD & trajectory solvers",
        "ethical_considerations": ["ITAR compliance", "airspace regulations", "space debris"]
    },
    "Energy Research": {
        "category": "Physical Sciences",
        "keywords": ["renewable energy", "solar cells", "battery storage", "wind turbine", "photovoltaic", "energy efficiency", "smart grid", "hydrogen fuel"],
        "default_methodology": "simulation",
        "evidence_types": ["power output profiles", "energy density measurements", "cycle life degradation"],
        "data_requirements": ["solar irradiance records", "grid demand time series"],
        "computational_needs": "Grid and electrochemical simulation tools",
        "ethical_considerations": ["resource extraction ethics (lithium/cobalt)", "grid reliability"]
    },

    # ── Earth & Life Sciences ────────────────────────────────────────────────
    "Earth Observation and Remote Sensing": {
        "category": "Earth & Life Sciences",
        "keywords": ["sentinel-1", "sentinel-2", "sar", "synthetic aperture radar", "change detection", "speckle noise", "satellite imagery", "copernicus", "remote sensing", "radiant mlhub"],
        "default_methodology": "computational",
        "evidence_types": ["orthorectified satellite imagery", "ground-truth change masks", "confusion matrices", "spatial tile partitions"],
        "data_requirements": ["multitemporal SAR / multispectral bands", "spatial coordinate bounds (GeoTIFF)"],
        "computational_needs": "TorchGeo / Rasterio / GDAL / PyTorch",
        "ethical_considerations": ["spatial autocorrelation data leakage", "surveillance privacy", "open earth observation licenses"]
    },
    "Geology and Geography": {
        "category": "Earth & Life Sciences",
        "keywords": ["geomorphology", "gis", "stratigraphy", "tectonics", "mineralogy", "cartography", "hydrology", "geopandas"],
        "default_methodology": "observational",
        "evidence_types": ["geological surveys", "spatial shapefiles", "stratigraphic columns"],
        "data_requirements": ["DEM elevation rasters", "geochemical assay records"],
        "computational_needs": "QGIS / GeoPandas / spatial statistics",
        "ethical_considerations": ["indigenous land rights", "extractive environmental impacts"]
    },
    "Climate Science": {
        "category": "Earth & Life Sciences",
        "keywords": ["climate change", "greenhouse gases", "cmip6", "global warming", "carbon cycle", "extreme weather", "paleoclimatology", "temperature anomaly"],
        "default_methodology": "simulation",
        "evidence_types": ["gridded climate reanalysis (ERA5)", "ice core records", "radiative forcing models"],
        "data_requirements": ["NetCDF / Xarray climate datasets", "meteorological sensor grids"],
        "computational_needs": "Xarray / NetCDF4 / parallel climate simulators",
        "ethical_considerations": ["scientific communication integrity", "policy implications"]
    },
    "Environmental Science": {
        "category": "Earth & Life Sciences",
        "keywords": ["ecosystem", "biodiversity", "pollution", "water quality", "conservation", "deforestation", "soil degradation", "microplastics"],
        "default_methodology": "observational",
        "evidence_types": ["field sample assays", "species occurrence records", "contaminant concentration logs"],
        "data_requirements": ["GBIF records", "EPA / WHO environmental monitoring feeds"],
        "computational_needs": "Ecological niche modeling / statistical packages",
        "ethical_considerations": ["habitat preservation during field work", "open data sharing"]
    },
    "Agriculture": {
        "category": "Earth & Life Sciences",
        "keywords": ["crop health", "ndvi", "precision agriculture", "crop yield", "soil moisture", "pest management", "irrigation", "agronomy"],
        "default_methodology": "computational",
        "evidence_types": ["multispectral vegetation indices", "yield records", "soil sensor telemetry"],
        "data_requirements": ["field boundary polygons", "harvest monitoring tables"],
        "computational_needs": "Computer vision / time-series regression",
        "ethical_considerations": ["farmer data ownership", "food security impacts"]
    },
    "Biology": {
        "category": "Earth & Life Sciences",
        "keywords": ["genetics", "evolution", "cellular biology", "ecology", "molecular biology", "microbiology", "protein folding", "genomics"],
        "default_methodology": "experimental",
        "evidence_types": ["sequencing FASTQ/FASTA files", "fluorescence microscopy", "phylogenetic trees"],
        "data_requirements": ["GenBank / UniProt records", "PCR / Western blot assays"],
        "computational_needs": "BioPython / BLAST / sequence alignment suites",
        "ethical_considerations": ["genetic privacy", "biosafety levels (BSL)", "dual-use pathogens"]
    },
    "Biotechnology": {
        "category": "Earth & Life Sciences",
        "keywords": ["crispr", "gene editing", "fermentation", "bioreactor", "recombinant dna", "synthetic biology", "metabolic engineering", "biopharmaceuticals"],
        "default_methodology": "experimental",
        "evidence_types": ["plasmid maps", "metabolic flux distributions", "growth kinetics"],
        "data_requirements": ["synthetic construct libraries", "HPLC purification chromatograms"],
        "computational_needs": "Bioinformatics pipelines / metabolic network solvers",
        "ethical_considerations": ["gene drive release risks", "bioethics review", "IP & patent barriers"]
    },

    # ── Medical & Healthcare Sciences ────────────────────────────────────────
    "Medicine and Healthcare": {
        "category": "Health & Medical",
        "keywords": ["clinical trial", "diagnosis", "liver disease", "cardiology", "oncology", "epidemiology", "patient outcome", "monai", "pathology", "ehr", "medical imaging"],
        "default_methodology": "observational",
        "evidence_types": ["clinical study registries (ClinicalTrials.gov)", "DICOM / NIfTI scans", "biochemical panels", "cohort survival data"],
        "data_requirements": ["de-identified patient records", "IRB-approved cohort access", "ICD-10 / LOINC coding"],
        "computational_needs": "MONAI / PyHealth / survival analysis packages",
        "ethical_considerations": ["HIPAA / GDPR patient confidentiality", "IRB ethics committee approval mandatory", "no diagnostic claims without peer validation", "vulnerable populations"]
    },
    "Pharmaceutical Research": {
        "category": "Health & Medical",
        "keywords": ["drug discovery", "pharmacokinetics", "pharmacodynamics", "molecular docking", "toxicology", "adme", "clinical trials", "qsar"],
        "default_methodology": "computational",
        "evidence_types": ["binding affinity Kd/IC50", "docking poses", "toxicity assays", "bioequivalence metrics"],
        "data_requirements": ["ChEMBL / BindingDB datasets", "PDB protein ligand complexes"],
        "computational_needs": "AutoDock / RDKit / molecular dynamics suites",
        "ethical_considerations": ["Good Clinical Practice (GCP)", "animal welfare compliance (IACUC)", "drug safety reporting"]
    },

    # ── Social Sciences & Humanities ─────────────────────────────────────────
    "Economics": {
        "category": "Social Sciences",
        "keywords": ["inflation", "econometrics", "macroeconomics", "microeconomics", "interest rates", "monetary policy", "gdp", "time-series", "forecasting", "statsmodels"],
        "default_methodology": "observational",
        "evidence_types": ["FRED time-series series", "VAR / ARIMA model outputs", "instrumental variable regressions"],
        "data_requirements": ["quarterly/monthly macroeconomic series", "household survey microdata"],
        "computational_needs": "Statsmodels / R / Pandas / econometric libraries",
        "ethical_considerations": ["causality vs correlation caveats", "policy recommendation objectivity", "reproducible empirical data"]
    },
    "Finance": {
        "category": "Social Sciences",
        "keywords": ["asset pricing", "portfolio optimization", "risk management", "financial derivatives", "volatility", "algorithmic trading", "corporate finance", "black-scholes"],
        "default_methodology": "computational",
        "evidence_types": ["historical tick/daily OHLCV prices", "Sharpe ratio / maximum drawdown", "VaR distributions"],
        "data_requirements": ["exchange order books", "financial statement filings (10-K)"],
        "computational_needs": "High-throughput financial modeling libraries",
        "ethical_considerations": ["market manipulation risks", "financial model overfitting", "systemic risk"]
    },
    "Business and Management": {
        "category": "Social Sciences",
        "keywords": ["supply chain", "organizational behavior", "strategic management", "marketing analytics", "operations research", "human resources", "entrepreneurship"],
        "default_methodology": "mixed_methods",
        "evidence_types": ["case study reports", "Likert scale surveys", "process optimization logs"],
        "data_requirements": ["firm-level survey responses", "operational enterprise ERP logs"],
        "computational_needs": "Statistical analysis / qualitative coding",
        "ethical_considerations": ["commercial confidentiality", "informed consent of employees"]
    },
    "Psychology": {
        "category": "Social Sciences",
        "keywords": ["student motivation", "cognitive psychology", "behavioral", "psychometrics", "mental health", "learning outcomes", "depression", "systematic review", "digital learning"],
        "default_methodology": "systematic_review",
        "evidence_types": ["PRISMA screening matrices", "psychometric validated scales (Likert)", "effect size Cohen's d", "forest plots"],
        "data_requirements": ["blinded participant questionnaires", "experimental response latency logs"],
        "computational_needs": "Statistical packages (SciPy / statsmodels / meta-analysis)",
        "ethical_considerations": ["IRB approval mandatory for human subjects", "debriefing protocols", "vulnerable youth participant protection"]
    },
    "Sociology": {
        "category": "Social Sciences",
        "keywords": ["demographics", "social stratification", "inequality", "urban sociology", "cultural studies", "census", "community studies", "ethnography"],
        "default_methodology": "mixed_methods",
        "evidence_types": ["census microdata", "in-depth interview transcripts", "field ethnographies"],
        "data_requirements": ["public demographic registers (IPUMS)", "transcribed field notes"],
        "computational_needs": "Qualitative coding software & survey analysis",
        "ethical_considerations": ["participant anonymization", "avoiding stigmatization of marginalized communities"]
    },
    "Political Science": {
        "category": "Social Sciences",
        "keywords": ["elections", "public policy", "international relations", "voting behavior", "governance", "political economy", "comparative politics", "legislation"],
        "default_methodology": "observational",
        "evidence_types": ["voting roll-call records", "polling microdata", "policy textual corpora"],
        "data_requirements": ["parliamentary proceedings", "electoral returns"],
        "computational_needs": "Text-as-data NLP & econometric estimators",
        "ethical_considerations": ["partisan neutrality", "handling sensitive polling data"]
    },
    "Education": {
        "category": "Social Sciences",
        "keywords": ["pedagogy", "digital learning", "curriculum", "educational technology", "learning outcomes", "classroom intervention", "assessment"],
        "default_methodology": "mixed_methods",
        "evidence_types": ["pre/post test standardized scores", "classroom observation rubrics", "learning management system telemetry"],
        "data_requirements": ["de-identified student cohort grades", "teacher interview transcripts"],
        "computational_needs": "ANOVA / mixed-effects regression / qualitative coding",
        "ethical_considerations": ["FERPA / pupil privacy laws", "parental informed consent for minors"]
    },
    "History": {
        "category": "Humanities",
        "keywords": ["historiography", "archival research", "primary sources", "historical analysis", "diplomatics", "oral history", "chronology"],
        "default_methodology": "qualitative",
        "evidence_types": ["archival documents", "contemporary letters/diaries", "historical maps", "material artifacts"],
        "data_requirements": ["digitized archival collections", "cataloged primary source facsimiles"],
        "computational_needs": "Digital humanities OCR & text alignment",
        "ethical_considerations": ["provenance and cultural heritage respect", "contextual representation integrity"]
    },
    "Linguistics": {
        "category": "Humanities",
        "keywords": ["phonetics", "syntax", "semantics", "sociolinguistics", "corpus linguistics", "morphology", "pragmatics", "language acquisition"],
        "default_methodology": "observational",
        "evidence_types": ["annotated speech corpora", "syntactic dependency trees", "acoustic spectrograms"],
        "data_requirements": ["Corpus of Contemporary American English (COCA)", "phonetic audio recordings"],
        "computational_needs": "Corpus query tools / Praat / NLP parsers",
        "ethical_considerations": ["linguistic diversity preservation", "speaker consent"]
    },
    "Law": {
        "category": "Humanities",
        "keywords": ["jurisprudence", "constitutional law", "legal theory", "statutory interpretation", "case law", "intellectual property", "international law"],
        "default_methodology": "qualitative",
        "evidence_types": ["judicial opinions (precedents)", "statutory codes", "legislative history records", "law review treatises"],
        "data_requirements": ["court dockets (CourtListener)", "treaty registers"],
        "computational_needs": "Legal corpus retrieval & citation network analyzers",
        "ethical_considerations": ["legal privilege", "accurate representation of active litigation"]
    },
    "Humanities": {
        "category": "Humanities",
        "keywords": ["philosophy", "ethics", "literature", "art history", "religious studies", "cultural criticism", "hermeneutics", "epistemology"],
        "default_methodology": "qualitative",
        "evidence_types": ["philosophical treatises", "literary texts", "artistic reproductions", "interpretative commentary"],
        "data_requirements": ["open access canonical texts", "digital museum collections"],
        "computational_needs": "Text analysis / citation analysis",
        "ethical_considerations": ["cultural sensitivity", "copyright in fair use criticism"]
    },
    "Interdisciplinary Research": {
        "category": "Interdisciplinary",
        "keywords": ["interdisciplinary", "multidisciplinary", "socio-technical", "bioinformatics", "digital humanities", "neuroeconomics", "environmental economics"],
        "default_methodology": "mixed_methods",
        "evidence_types": ["integrated multi-source evidence", "cross-domain validation metrics"],
        "data_requirements": ["heterogeneous multi-modal datasets"],
        "computational_needs": "Flexible modular analytical toolchains",
        "ethical_considerations": ["harmonization of divergent disciplinary ethical standards"]
    }
}


class UniversalDomainRouter:
    """
    Intelligently classifies scientific research topics into primary and secondary domains,
    recommends scientific methodologies, expands keywords, and identifies regulatory/data needs.
    """

    def __init__(self):
        self.semantic_search = SemanticSearchEngine()

    def classify_topic(
        self,
        topic: str,
        abstract_context: Optional[str] = None,
        user_override_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main domain routing method.
        Scans topic against all 36 domains using semantic cosine vectors + lexical keyword scoring.
        """
        text = f"{topic} {abstract_context or ''}".lower()
        topic_vec = self.semantic_search.compute_embedding(text)

        domain_scores: List[Dict[str, Any]] = []

        for domain_name, meta in RESEARCH_DOMAINS.items():
            # 1. Lexical keyword matching score
            matched_keywords = []
            for kw in meta["keywords"]:
                if re.search(r'\b' + re.escape(kw) + r'\b', text):
                    matched_keywords.append(kw)

            keyword_score = len(matched_keywords) * 0.35

            # 2. Semantic vector cosine similarity against domain descriptor
            domain_descriptor = f"{domain_name} {meta['category']} {' '.join(meta['keywords'])}"
            d_vec = self.semantic_search.compute_embedding(domain_descriptor)
            sim = self.semantic_search.cosine_similarity(topic_vec, d_vec)

            # Combined score with keyword reinforcement
            total_score = round(min(1.0, (sim * 0.55) + min(0.45, keyword_score)), 3)

            domain_scores.append({
                "domain": domain_name,
                "category": meta["category"],
                "score": total_score,
                "matched_keywords": matched_keywords,
                "metadata": meta
            })

        # Sort descending by relevance score
        domain_scores.sort(key=lambda x: x["score"], reverse=True)

        # Handle user manual override if provided
        if user_override_domain and user_override_domain in RESEARCH_DOMAINS:
            primary_domain = user_override_domain
            primary_meta = RESEARCH_DOMAINS[user_override_domain]
            confidence = 1.0
            secondary_domains = [d["domain"] for d in domain_scores if d["domain"] != primary_domain][:3]
        else:
            top_hit = domain_scores[0]
            primary_domain = top_hit["domain"]
            primary_meta = top_hit["metadata"]
            confidence = top_hit["score"]
            secondary_domains = [d["domain"] for d in domain_scores[1:4] if d["score"] > 0.25]

        # Generate query expansions
        query_expansions = self._generate_query_expansions(topic, primary_meta["keywords"])

        return {
            "topic": topic,
            "classified_at": datetime.now(timezone.utc).isoformat(),
            "primary_domain": primary_domain,
            "category": primary_meta["category"],
            "classification_confidence": confidence,
            "secondary_domains": secondary_domains,
            "default_methodology": primary_meta["default_methodology"],
            "relevant_subfields": primary_meta["keywords"][:5],
            "research_keywords": list(set([w for w in re.findall(r'\b\w{4,}\b', topic.lower()) if w not in {"with", "from", "using", "that", "this", "deep", "methods"}][:6] + primary_meta["keywords"][:4])),
            "query_expansions": query_expansions,
            "evidence_requirements": primary_meta["evidence_types"],
            "dataset_requirements": primary_meta["data_requirements"],
            "computational_needs": primary_meta["computational_needs"],
            "ethical_and_regulatory_considerations": primary_meta["ethical_considerations"],
            "domain_override_supported": True,
            "taxonomy_version": "P-Research-OS-Omega-36"
        }

    def _generate_query_expansions(self, topic: str, keywords: List[str]) -> List[str]:
        """Expands research topic into tailored academic search queries."""
        expansions = [topic]
        clean_topic = re.sub(r'[^\w\s]', '', topic)
        words = clean_topic.split()

        if len(words) >= 2:
            expansions.append(f"{words[0]} {words[1]} methodology review")

        for kw in keywords[:3]:
            expansions.append(f"{clean_topic} {kw}")

        return list(dict.fromkeys(expansions))[:5]


universal_domain_router = UniversalDomainRouter()

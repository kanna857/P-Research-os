-- =============================================================================
-- ResearchOS: Nhost + PostgreSQL + pgvector Complete Database Migration
-- Version: 001_nhost_complete_schema.sql
-- Enables: uuid-ossp, pgcrypto, citext, and pgvector for semantic search
-- =============================================================================

-- 1. Enable Required Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 2. Ensure Nhost Schemas exist (if running in standalone Postgres)
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS storage;
CREATE SCHEMA IF NOT EXISTS public;

-- 3. Users Table (Nhost Compatible)
CREATE TABLE IF NOT EXISTS public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON public.users(username);

-- 4. User Profiles Table
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    institution VARCHAR(255),
    orcid VARCHAR(64),
    bio TEXT,
    research_interests JSONB DEFAULT '[]'::jsonb,
    h_index INTEGER DEFAULT 0,
    avatar_url VARCHAR(1000),
    role VARCHAR(50) DEFAULT 'user' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON public.user_profiles(user_id);

-- 5. Research Projects Table
CREATE TABLE IF NOT EXISTS public.projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    research_topic VARCHAR(500),
    keywords JSONB DEFAULT '{}'::jsonb,
    target_journal VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' NOT NULL,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON public.projects(user_id);
CREATE INDEX IF NOT EXISTS idx_projects_status ON public.projects(status);

-- 6. Research Topics Table
CREATE TABLE IF NOT EXISTS public.research_topics (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    topic_title VARCHAR(500) NOT NULL,
    domain_tags JSONB DEFAULT '[]'::jsonb,
    expanded_queries JSONB DEFAULT '[]'::jsonb,
    status VARCHAR(50) DEFAULT 'active' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_research_topics_project_id ON public.research_topics(project_id);

-- 7. Papers Table
CREATE TABLE IF NOT EXISTS public.papers (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    authors JSONB DEFAULT '[]'::jsonb,
    abstract TEXT,
    doi VARCHAR(255),
    year INTEGER,
    venue VARCHAR(500),
    citation_count INTEGER DEFAULT 0,
    source VARCHAR(100),
    pdf_url VARCHAR(1000),
    pdf_path VARCHAR(1000),
    is_open_access BOOLEAN DEFAULT FALSE,
    download_status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_papers_project_id ON public.papers(project_id);
CREATE INDEX IF NOT EXISTS idx_papers_doi ON public.papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_title ON public.papers(title);

-- 8. Paper Authors Table
CREATE TABLE IF NOT EXISTS public.paper_authors (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER NOT NULL REFERENCES public.papers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    affiliation VARCHAR(500),
    orcid VARCHAR(64),
    author_order INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_paper_authors_paper_id ON public.paper_authors(paper_id);

-- 9. Citations Table
CREATE TABLE IF NOT EXISTS public.citations (
    id SERIAL PRIMARY KEY,
    paper_id INTEGER NOT NULL REFERENCES public.papers(id) ON DELETE CASCADE,
    citation_text TEXT NOT NULL,
    doi VARCHAR(255),
    year INTEGER,
    context_snippet TEXT
);
CREATE INDEX IF NOT EXISTS idx_citations_paper_id ON public.citations(paper_id);

-- 10. Datasets Table
CREATE TABLE IF NOT EXISTS public.datasets (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source VARCHAR(100),
    source_url VARCHAR(1000),
    license VARCHAR(255),
    total_samples INTEGER,
    classes JSONB DEFAULT '{}'::jsonb,
    image_width INTEGER,
    image_height INTEGER,
    channels INTEGER,
    file_format VARCHAR(50),
    download_size VARCHAR(50),
    local_path VARCHAR(1000),
    status VARCHAR(50) DEFAULT 'registered' NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_datasets_project_id ON public.datasets(project_id);

-- 11. Processed Datasets (80/20 non-leaking partitions)
CREATE TABLE IF NOT EXISTS public.processed_datasets (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES public.datasets(id) ON DELETE CASCADE,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    config JSONB DEFAULT '{}'::jsonb,
    train_count INTEGER,
    test_count INTEGER,
    output_path VARCHAR(1000),
    version VARCHAR(50),
    status VARCHAR(50) DEFAULT 'pending' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_processed_datasets_dataset ON public.processed_datasets(dataset_id);
CREATE INDEX IF NOT EXISTS idx_processed_datasets_project ON public.processed_datasets(project_id);

-- 12. Dataset Versions
CREATE TABLE IF NOT EXISTS public.dataset_versions (
    id SERIAL PRIMARY KEY,
    dataset_id INTEGER NOT NULL REFERENCES public.datasets(id) ON DELETE CASCADE,
    version_tag VARCHAR(50) NOT NULL,
    sample_count INTEGER DEFAULT 0,
    train_count INTEGER DEFAULT 0,
    test_count INTEGER DEFAULT 0,
    split_strategy VARCHAR(100) DEFAULT '80_20_stratified_non_leaking',
    storage_uri VARCHAR(1000),
    sha256_manifest VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_dataset_versions_dataset_id ON public.dataset_versions(dataset_id);

-- 13. Paper-to-Dataset Links (Bipartite Graph)
CREATE TABLE IF NOT EXISTS public.paper_dataset_links (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    paper_id INTEGER REFERENCES public.papers(id) ON DELETE SET NULL,
    dataset_id INTEGER REFERENCES public.datasets(id) ON DELETE SET NULL,
    paper_title VARCHAR(500) NOT NULL,
    dataset_name VARCHAR(255) NOT NULL,
    dataset_source VARCHAR(100) DEFAULT 'scientific_repository',
    official_source_url VARCHAR(1000),
    is_labeled_benchmark BOOLEAN DEFAULT TRUE,
    training_suitability VARCHAR(50) DEFAULT 'HIGH_TRAINING_READY',
    suitability_rationale TEXT,
    confidence_score FLOAT DEFAULT 0.95,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_paper_dataset_links_project ON public.paper_dataset_links(project_id);

-- 14. Autonomous Research Jobs Table
CREATE TABLE IF NOT EXISTS public.research_jobs (
    id VARCHAR(64) PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    job_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'queued' NOT NULL,
    progress_pct FLOAT DEFAULT 0.0,
    current_step VARCHAR(255),
    retries_count INTEGER DEFAULT 0,
    error_message TEXT,
    result_payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_research_jobs_project_status ON public.research_jobs(project_id, status);

-- 15. Research Agents Table
CREATE TABLE IF NOT EXISTS public.research_agents (
    id VARCHAR(64) PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    agent_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'idle',
    current_perspective VARCHAR(255),
    memory_state JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_research_agents_project ON public.research_agents(project_id);

-- 16. Agent Execution Logs
CREATE TABLE IF NOT EXISTS public.agent_execution_logs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(64) NOT NULL REFERENCES public.research_jobs(id) ON DELETE CASCADE,
    agent_id VARCHAR(64),
    step_name VARCHAR(255) NOT NULL,
    log_level VARCHAR(20) DEFAULT 'INFO',
    message TEXT NOT NULL,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_agent_logs_job ON public.agent_execution_logs(job_id);

-- 17. ML Models Table
CREATE TABLE IF NOT EXISTS public.ml_models (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    family VARCHAR(100),
    architecture VARCHAR(255),
    config JSONB DEFAULT '{}'::jsonb,
    code_path VARCHAR(1000),
    pretrained BOOLEAN DEFAULT TRUE NOT NULL,
    status VARCHAR(50) DEFAULT 'registered' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ml_models_project ON public.ml_models(project_id);

-- 18. Training Jobs Table
CREATE TABLE IF NOT EXISTS public.training_jobs (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    model_id INTEGER NOT NULL REFERENCES public.ml_models(id) ON DELETE CASCADE,
    dataset_id INTEGER NOT NULL REFERENCES public.processed_datasets(id) ON DELETE CASCADE,
    config JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'queued' NOT NULL,
    current_epoch INTEGER DEFAULT 0,
    total_epochs INTEGER,
    metrics JSONB DEFAULT '{}'::jsonb,
    checkpoint_path VARCHAR(1000),
    logs_path VARCHAR(1000),
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_training_jobs_project ON public.training_jobs(project_id);

-- 19. Experiments Table
CREATE TABLE IF NOT EXISTS public.experiments (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    training_job_id INTEGER NOT NULL REFERENCES public.training_jobs(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    metrics JSONB DEFAULT '{}'::jsonb,
    artifacts JSONB DEFAULT '{}'::jsonb,
    comparison_group VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experiments_project ON public.experiments(project_id);

-- 20. Experiment Metrics Table
CREATE TABLE IF NOT EXISTS public.experiment_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER NOT NULL REFERENCES public.experiments(id) ON DELETE CASCADE,
    epoch INTEGER NOT NULL,
    step INTEGER DEFAULT 0,
    train_loss FLOAT,
    val_loss FLOAT,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    iou FLOAT,
    dice FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_experiment_metrics_exp_epoch ON public.experiment_metrics(experiment_id, epoch);

-- 21. Training Checkpoints Table
CREATE TABLE IF NOT EXISTS public.training_checkpoints (
    id SERIAL PRIMARY KEY,
    experiment_id INTEGER NOT NULL REFERENCES public.experiments(id) ON DELETE CASCADE,
    epoch INTEGER NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    val_loss FLOAT,
    val_f1 FLOAT,
    sha256_checksum VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_training_checkpoints_exp ON public.training_checkpoints(experiment_id);

-- 22. Generated Figures Table
CREATE TABLE IF NOT EXISTS public.generated_figures (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    experiment_id INTEGER REFERENCES public.experiments(id) ON DELETE SET NULL,
    figure_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    storage_path VARCHAR(1000) NOT NULL,
    nhost_file_id VARCHAR(128),
    format VARCHAR(20) DEFAULT 'png',
    sha256_checksum VARCHAR(64),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_generated_figures_project ON public.generated_figures(project_id);

-- 23. Manuscripts Table
CREATE TABLE IF NOT EXISTS public.manuscripts (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    target_journal VARCHAR(255),
    sections JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'draft' NOT NULL,
    word_count INTEGER DEFAULT 0,
    compiled_pdf_path VARCHAR(1000),
    latex_source_path VARCHAR(1000),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_manuscripts_project ON public.manuscripts(project_id);

-- 24. Manuscript Versions Table
CREATE TABLE IF NOT EXISTS public.manuscript_versions (
    id SERIAL PRIMARY KEY,
    manuscript_id INTEGER NOT NULL REFERENCES public.manuscripts(id) ON DELETE CASCADE,
    version_number INTEGER DEFAULT 1,
    title VARCHAR(500) NOT NULL,
    latex_content TEXT NOT NULL,
    compiled_pdf_path VARCHAR(1000),
    changelog TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_manuscript_versions_manuscript ON public.manuscript_versions(manuscript_id);

-- 25. Research Artifacts Table
CREATE TABLE IF NOT EXISTS public.research_artifacts (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES public.projects(id) ON DELETE CASCADE,
    artifact_name VARCHAR(255) NOT NULL,
    artifact_type VARCHAR(100) NOT NULL,
    summary TEXT NOT NULL,
    file_path VARCHAR(1000),
    user_facing BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_research_artifacts_project ON public.research_artifacts(project_id);

-- 26. Notifications Table
CREATE TABLE IF NOT EXISTS public.notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    type VARCHAR(50) DEFAULT 'info',
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON public.notifications(user_id, is_read);

-- 27. Audit Logs Table
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES public.users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(100) NOT NULL,
    entity_id VARCHAR(128),
    ip_address VARCHAR(64),
    user_agent VARCHAR(500),
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_action ON public.audit_logs(user_id, action);

-- 28. API Provider Usage Table
CREATE TABLE IF NOT EXISTS public.api_provider_usage (
    id VARCHAR(64) PRIMARY KEY,
    provider_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    is_free_tier BOOLEAN DEFAULT TRUE,
    request_count INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    last_status VARCHAR(50) DEFAULT 'healthy',
    latency_ms INTEGER,
    quota_info VARCHAR(255),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- 29. pgvector Paper Embeddings Table
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        CREATE TABLE IF NOT EXISTS public.paper_embeddings (
            id SERIAL PRIMARY KEY,
            paper_id INTEGER NOT NULL REFERENCES public.papers(id) ON DELETE CASCADE,
            chunk_index INTEGER DEFAULT 0,
            chunk_type VARCHAR(50) DEFAULT 'abstract',
            content_text TEXT NOT NULL,
            embedding vector(384),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_paper_embeddings_vector ON public.paper_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
        CREATE INDEX IF NOT EXISTS idx_paper_embeddings_lookup ON public.paper_embeddings(paper_id, chunk_index);
    END IF;
END $$;

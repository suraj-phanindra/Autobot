-- ============================================================================
-- AutoBot: Natural Language Vehicle Inventory Search
-- Initial Database Schema Migration
-- ============================================================================

-- ============================================================================
-- EXTENSIONS
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================================================
-- TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- tenants
-- ----------------------------------------------------------------------------

CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    logo_url TEXT,
    primary_color TEXT DEFAULT '#2563eb',
    plan TEXT NOT NULL DEFAULT 'free',
    settings JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- users
-- ----------------------------------------------------------------------------

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    supabase_auth_id UUID NOT NULL UNIQUE,
    email TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'member',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_supabase_auth_id ON users(supabase_auth_id);

-- ----------------------------------------------------------------------------
-- vehicles
-- ----------------------------------------------------------------------------

CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    vin VARCHAR(17),
    stock_number TEXT,
    year INTEGER,
    make TEXT,
    model TEXT,
    trim TEXT,
    body_style TEXT,
    engine_type TEXT,
    engine_cylinders INTEGER,
    displacement_l DOUBLE PRECISION,
    horsepower INTEGER,
    torque INTEGER,
    drive_type TEXT,
    transmission TEXT,
    fuel_type TEXT,
    exterior_color TEXT,
    interior_color TEXT,
    mileage INTEGER,
    price NUMERIC(12, 2),
    msrp NUMERIC(12, 2),
    condition TEXT,
    accident_count INTEGER NOT NULL DEFAULT 0,
    owner_count INTEGER NOT NULL DEFAULT 0,
    title_status TEXT,
    has_recalls BOOLEAN NOT NULL DEFAULT FALSE,
    factory_options JSONB NOT NULL DEFAULT '[]',
    packages JSONB NOT NULL DEFAULT '[]',
    safety_features JSONB NOT NULL DEFAULT '[]',
    nhtsa_raw JSONB,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    search_vector TSVECTOR,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_vehicles_tenant_id ON vehicles(tenant_id);
CREATE INDEX idx_vehicles_vin ON vehicles(vin);
CREATE INDEX idx_vehicles_tenant_status ON vehicles(tenant_id, status);
CREATE INDEX idx_vehicles_search_vector ON vehicles USING GIN(search_vector);
CREATE INDEX idx_vehicles_make_model ON vehicles(make, model);
CREATE INDEX idx_vehicles_year ON vehicles(year);

-- ----------------------------------------------------------------------------
-- documents
-- ----------------------------------------------------------------------------

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    filename TEXT NOT NULL,
    file_type TEXT,
    file_size_bytes INTEGER,
    storage_path TEXT NOT NULL,
    source_type TEXT NOT NULL DEFAULT 'upload',
    processing_status TEXT NOT NULL DEFAULT 'pending',
    extracted_text TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_documents_tenant_id ON documents(tenant_id);
CREATE INDEX idx_documents_vehicle_id ON documents(vehicle_id);
CREATE INDEX idx_documents_processing_status ON documents(processing_status);

-- ----------------------------------------------------------------------------
-- document_chunks
-- ----------------------------------------------------------------------------

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk_type TEXT NOT NULL DEFAULT 'text',
    embedding vector(1536),
    search_vector TSVECTOR,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_document_chunks_tenant_id ON document_chunks(tenant_id);
CREATE INDEX idx_document_chunks_document_id ON document_chunks(document_id);
CREATE INDEX idx_document_chunks_vehicle_id ON document_chunks(vehicle_id);
CREATE INDEX idx_document_chunks_embedding ON document_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_document_chunks_search_vector ON document_chunks USING GIN(search_vector);

-- ----------------------------------------------------------------------------
-- search_logs
-- ----------------------------------------------------------------------------

CREATE TABLE search_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    query_text TEXT NOT NULL,
    query_source TEXT NOT NULL DEFAULT 'dashboard',
    intent JSONB,
    result_count INTEGER NOT NULL DEFAULT 0,
    vehicle_ids JSONB NOT NULL DEFAULT '[]',
    chunk_ids JSONB NOT NULL DEFAULT '[]',
    response_text TEXT,
    search_duration_ms INTEGER,
    llm_duration_ms INTEGER,
    total_duration_ms INTEGER,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_text TEXT,
    session_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_search_logs_tenant_id ON search_logs(tenant_id);
CREATE INDEX idx_search_logs_created_at ON search_logs(created_at);

-- ----------------------------------------------------------------------------
-- api_keys
-- ----------------------------------------------------------------------------

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    key_prefix VARCHAR(8) NOT NULL,
    key_hash TEXT NOT NULL,
    scopes JSONB NOT NULL DEFAULT '["widget:query"]',
    allowed_origins JSONB NOT NULL DEFAULT '[]',
    rate_limit_per_minute INTEGER NOT NULL DEFAULT 30,
    rate_limit_per_day INTEGER NOT NULL DEFAULT 10000,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_api_keys_tenant_id ON api_keys(tenant_id);
CREATE INDEX idx_api_keys_key_hash ON api_keys(key_hash);

-- ----------------------------------------------------------------------------
-- conversations
-- ----------------------------------------------------------------------------

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
    session_id TEXT NOT NULL,
    messages JSONB NOT NULL DEFAULT '[]',
    vehicle_context JSONB NOT NULL DEFAULT '[]',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_conversations_tenant_id ON conversations(tenant_id);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);

-- ============================================================================
-- TRIGGERS: Auto-update updated_at
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_tenants_updated_at BEFORE UPDATE ON tenants FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_vehicles_updated_at BEFORE UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_documents_updated_at BEFORE UPDATE ON documents FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER tr_conversations_updated_at BEFORE UPDATE ON conversations FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================================
-- TRIGGERS: Auto-generate search_vector for vehicles
-- ============================================================================

CREATE OR REPLACE FUNCTION vehicles_search_vector_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.make, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.model, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.trim, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.body_style, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.engine_type, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.drive_type, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.fuel_type, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.exterior_color, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.interior_color, '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.condition, '')), 'D') ||
        setweight(to_tsvector('english', COALESCE(NEW.notes, '')), 'D') ||
        setweight(to_tsvector('english', COALESCE(NEW.title_status, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_vehicles_search_vector BEFORE INSERT OR UPDATE ON vehicles FOR EACH ROW EXECUTE FUNCTION vehicles_search_vector_update();

-- ============================================================================
-- TRIGGERS: Auto-generate search_vector for document_chunks
-- ============================================================================

CREATE OR REPLACE FUNCTION document_chunks_search_vector_update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := to_tsvector('english', COALESCE(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_document_chunks_search_vector BEFORE INSERT OR UPDATE ON document_chunks FOR EACH ROW EXECUTE FUNCTION document_chunks_search_vector_update();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Helper function to extract tenant_id from JWT claims
CREATE OR REPLACE FUNCTION auth.tenant_id() RETURNS UUID AS $$
  SELECT COALESCE(
    (current_setting('request.jwt.claims', true)::jsonb ->> 'tenant_id')::uuid,
    '00000000-0000-0000-0000-000000000000'::uuid
  );
$$ LANGUAGE sql STABLE;

-- Enable RLS on all tenant-scoped tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Tenant isolation policies
CREATE POLICY users_tenant_isolation ON users FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY vehicles_tenant_isolation ON vehicles FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY documents_tenant_isolation ON documents FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY document_chunks_tenant_isolation ON document_chunks FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY search_logs_tenant_isolation ON search_logs FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY api_keys_tenant_isolation ON api_keys FOR ALL USING (tenant_id = auth.tenant_id());
CREATE POLICY conversations_tenant_isolation ON conversations FOR ALL USING (tenant_id = auth.tenant_id());

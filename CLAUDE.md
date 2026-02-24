# AutoBot - Natural Language Vehicle Inventory Search

## Project Overview
Multi-tenant SaaS for used car dealerships. Aggregates vehicle data (VIN decode, Carfax PDFs, spec sheets) and makes it queryable via natural language for dealership staff + embeddable website widget.

## Architecture
- **Backend**: FastAPI (Python, async) at `backend/`
- **Frontend**: Next.js 15 + TypeScript + Tailwind + shadcn/ui at `frontend/`
- **Widget**: Vite + React IIFE bundle with Shadow DOM at `packages/widget/`
- **Database**: Supabase (PostgreSQL + pgvector), migrations at `supabase/migrations/`
- **LLM**: Claude API (Sonnet) for intent classification + RAG generation
- **Embeddings**: OpenAI text-embedding-3-small (1536d)

## Key Patterns
- All database tables are tenant-scoped with RLS policies
- Backend uses async SQLAlchemy with Supabase PostgreSQL
- Auth via Supabase Auth (JWT verification in middleware)
- Hybrid search: BM25 (tsvector) + vector (pgvector) + RRF fusion
- Widget authenticates via X-API-Key header, rate-limited

## Commands
- **Backend**: `cd backend && poetry install && poetry run uvicorn app.main:app --reload`
- **Frontend**: `cd frontend && npm install && npm run dev`
- **Widget**: `cd packages/widget && npm install && npm run dev`
- **Migrations**: Applied via Supabase CLI or directly to Supabase dashboard

## Environment Variables
Backend `.env` needs: SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_JWT_SECRET, ANTHROPIC_API_KEY, OPENAI_API_KEY

## Conventions
- Python: async/await, type hints, Pydantic v2 for schemas
- TypeScript: strict mode, React Query for data fetching
- API routes: `/api/v1/` prefix, authenticated via Supabase JWT or API key
- All timestamps in UTC

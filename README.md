# AutoBot

Natural Language Vehicle Inventory Search Platform for used car dealerships.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker (for local development)
- Supabase account

### Backend
```bash
cd backend
poetry install
cp .env.example .env  # Fill in your keys
poetry run uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env.local  # Fill in your keys
npm run dev
```

### Widget
```bash
cd packages/widget
npm install
npm run dev
```

## Architecture

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python, async) |
| Frontend | Next.js 15 + TypeScript + Tailwind + shadcn/ui |
| Widget | Vite + React (IIFE bundle, Shadow DOM) |
| Database | Supabase (PostgreSQL + pgvector) |
| LLM | Claude API (Sonnet) |
| Embeddings | OpenAI text-embedding-3-small |
| Auth | Supabase Auth |


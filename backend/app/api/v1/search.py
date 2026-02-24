import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_tenant_id
from app.db.session import get_db
from app.schemas.search import SearchRequest, SearchResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.post("/", response_model=SearchResponse)
async def search_vehicles(
    request: SearchRequest,
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> SearchResponse:
    """Natural language search across the vehicle inventory.

    This endpoint will:
    1. Parse the natural language query to extract intent and filters.
    2. Perform hybrid search (semantic vector search + full-text search).
    3. Rank and re-rank results.
    4. Generate a natural language response via LLM.

    Currently returns a placeholder response. The full RAG pipeline will be
    implemented in the search_engine and rag_pipeline services.
    """
    return SearchResponse(
        query=request.query,
        response_text=(
            "Search is not yet implemented. This placeholder confirms the endpoint is wired up correctly."
        ),
        results=[],
        total_results=0,
        search_duration_ms=0,
        llm_duration_ms=None,
        total_duration_ms=0,
        session_id=request.session_id,
    )

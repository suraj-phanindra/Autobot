import uuid
from decimal import Decimal

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Natural language search request."""

    query: str = Field(..., min_length=1, max_length=1000, description="Natural language search query")
    max_results: int = Field(default=10, ge=1, le=50, description="Maximum number of results")
    session_id: str | None = Field(None, description="Conversation session ID for context")
    source: str = Field(default="dashboard", description="Source of the search request")

    model_config = {"from_attributes": True}


class SearchResultItem(BaseModel):
    """A single search result item."""

    vehicle_id: uuid.UUID
    score: float = Field(description="Relevance score")
    year: int | None = None
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    price: Decimal | None = None
    mileage: int | None = None
    exterior_color: str | None = None
    vin: str | None = None
    stock_number: str | None = None
    status: str | None = None
    match_reason: str | None = Field(None, description="Why this vehicle matched")

    model_config = {"from_attributes": True}


class SearchResponse(BaseModel):
    """Response from a search query."""

    query: str
    response_text: str | None = Field(None, description="AI-generated natural language response")
    results: list[SearchResultItem] = []
    total_results: int = 0
    search_duration_ms: int = 0
    llm_duration_ms: int | None = None
    total_duration_ms: int = 0
    session_id: str | None = None

    model_config = {"from_attributes": True}

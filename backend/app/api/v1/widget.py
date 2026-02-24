from fastapi import APIRouter, Header
from pydantic import BaseModel, Field

router = APIRouter(prefix="/widget", tags=["widget"])


class WidgetConfig(BaseModel):
    """Configuration returned to the embeddable widget."""

    tenant_name: str = ""
    primary_color: str = "#2563eb"
    welcome_message: str = "Hi! Ask me anything about our vehicle inventory."
    placeholder_text: str = "e.g. Show me SUVs under $30k with low mileage"
    max_results: int = 5
    branding_enabled: bool = True


class WidgetQueryRequest(BaseModel):
    """Incoming query from the embeddable widget."""

    query: str = Field(..., min_length=1, max_length=1000)
    session_id: str | None = None


class WidgetQueryResponse(BaseModel):
    """Response sent back to the embeddable widget."""

    response_text: str
    vehicles: list[dict] = []
    session_id: str | None = None


@router.get("/config", response_model=WidgetConfig)
async def get_widget_config(
    x_api_key: str = Header(..., description="Widget API key"),
) -> WidgetConfig:
    """Return widget configuration for the given API key.

    The API key identifies the tenant and determines the widget's appearance
    and behavior settings.

    This is a placeholder that returns default configuration. The full
    implementation will look up the tenant by API key and return their
    custom widget settings.
    """
    return WidgetConfig(
        tenant_name="Demo Dealership",
        primary_color="#2563eb",
        welcome_message="Hi! Ask me anything about our vehicle inventory.",
        placeholder_text="e.g. Show me SUVs under $30k with low mileage",
        max_results=5,
        branding_enabled=True,
    )


@router.post("/query", response_model=WidgetQueryResponse)
async def widget_query(
    request: WidgetQueryRequest,
    x_api_key: str = Header(..., description="Widget API key"),
) -> WidgetQueryResponse:
    """Process a natural language query from the embeddable widget.

    This endpoint is called by the JavaScript widget embedded on dealership
    websites. It authenticates via API key (not JWT) and applies the
    appropriate rate limits.

    This is a placeholder. The full implementation will:
    1. Validate the API key and resolve the tenant.
    2. Apply rate limiting.
    3. Run the query through the RAG pipeline.
    4. Log the search.
    5. Return results formatted for the widget.
    """
    return WidgetQueryResponse(
        response_text=(
            "Widget search is not yet implemented. "
            "This placeholder confirms the widget endpoint is wired up correctly."
        ),
        vehicles=[],
        session_id=request.session_id,
    )

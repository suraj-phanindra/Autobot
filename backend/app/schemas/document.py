import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class DocumentUpload(BaseModel):
    """Schema for document upload metadata."""

    filename: str = Field(..., max_length=500)
    file_type: str = Field(..., max_length=50)
    file_size_bytes: int = Field(..., gt=0)
    vehicle_id: uuid.UUID | None = None
    source_type: str = "upload"

    model_config = {"from_attributes": True}


class DocumentResponse(BaseModel):
    """Full document response schema."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    vehicle_id: uuid.UUID | None = None
    filename: str
    file_type: str
    file_size_bytes: int
    storage_path: str
    source_type: str
    processing_status: str
    extracted_text: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

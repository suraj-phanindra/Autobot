import uuid

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Decoded JWT token payload from Supabase."""

    sub: str  # Supabase auth user ID
    email: str | None = None
    role: str | None = None
    aud: str | None = None
    exp: int | None = None
    iat: int | None = None
    iss: str | None = None

    model_config = {"from_attributes": True}


class CurrentUser(BaseModel):
    """Represents the currently authenticated user."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    supabase_auth_id: str
    email: str
    full_name: str | None = None
    role: str = "member"

    model_config = {"from_attributes": True}

import uuid

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.core.security import verify_supabase_jwt
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import CurrentUser


async def get_current_user(
    authorization: str = Header(..., description="Bearer <token>"),
    db: AsyncSession = Depends(get_db),
) -> CurrentUser:
    """Extract and verify the Bearer JWT, then look up the corresponding user.

    This dependency:
    1. Parses the Authorization header for a Bearer token.
    2. Verifies the token against the Supabase JWT secret.
    3. Looks up the user in the database by their Supabase auth ID.
    4. Returns a CurrentUser schema instance.

    Raises:
        PermissionDeniedError: If the token is missing, invalid, or the user is not found.
    """
    if not authorization.startswith("Bearer "):
        raise PermissionDeniedError("Authorization header must start with 'Bearer '.")

    token = authorization[7:]  # Strip "Bearer " prefix
    payload = verify_supabase_jwt(token)
    supabase_auth_id = payload.get("sub")

    if not supabase_auth_id:
        raise PermissionDeniedError("Token payload missing 'sub' claim.")

    result = await db.execute(
        select(User).where(User.supabase_auth_id == supabase_auth_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise NotFoundError("User not found. Please complete onboarding first.")

    return CurrentUser(
        id=user.id,
        tenant_id=user.tenant_id,
        supabase_auth_id=user.supabase_auth_id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
    )


async def get_current_tenant_id(
    current_user: CurrentUser = Depends(get_current_user),
) -> uuid.UUID:
    """Convenience dependency that returns just the tenant_id for the current user."""
    return current_user.tenant_id

import hashlib
import secrets

from jose import JWTError, jwt

from app.config import get_settings
from app.core.exceptions import PermissionDeniedError


def verify_supabase_jwt(token: str) -> dict:
    """Decode and verify a Supabase JWT token.

    Args:
        token: The raw JWT string from the Authorization header.

    Returns:
        The decoded token payload as a dict.

    Raises:
        PermissionDeniedError: If the token is invalid or expired.
    """
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except JWTError as e:
        raise PermissionDeniedError(f"Invalid or expired token: {e}")


def hash_api_key(key: str) -> str:
    """Create a SHA-256 hash of an API key.

    Args:
        key: The raw API key string.

    Returns:
        Hex-encoded SHA-256 hash.
    """
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def generate_api_key() -> tuple[str, str]:
    """Generate a new API key and its hash.

    Returns:
        A tuple of (raw_key, key_hash). The raw key should be shown to the user
        once and never stored. The hash is stored in the database.
    """
    raw_key = f"ab_{secrets.token_urlsafe(32)}"
    key_hash = hash_api_key(raw_key)
    return raw_key, key_hash

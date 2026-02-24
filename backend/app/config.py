from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "AutoBot API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Supabase
    supabase_url: str
    supabase_service_key: str
    supabase_jwt_secret: str
    database_url: str  # postgresql+asyncpg://...

    # AI
    anthropic_api_key: str
    openai_api_key: str

    # Redis
    redis_url: str = "redis://localhost:6379"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    return Settings()

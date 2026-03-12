from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Supabase
    supabase_url: str
    supabase_service_key: str
    supabase_anon_key: str
    supabase_jwt_secret: str

    # OpenAI (embeddings)
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # Anthropic (LLM)
    anthropic_api_key: str
    llm_model: str = "claude-3-5-sonnet-20241022"

    # Upstash Redis (cache + rate limiting)
    upstash_redis_url: str = ""
    upstash_redis_token: str = ""

    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    # BetterStack
    betterstack_source_token: str = ""

    # API
    cors_origins: list[str] = ["http://localhost:3000"]
    api_rate_limit: int = 60  # requests per minute


settings = Settings()

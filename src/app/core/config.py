from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Bilingual DocQA API"
    environment: str = "local"
    debug: bool = False
    database_url: str
    test_database_url: str
    embedding_base_url: str
    embedding_model: str
    embedding_api_key: str = "ollama"
    embedding_dimensions: int = 1024


settings = Settings()

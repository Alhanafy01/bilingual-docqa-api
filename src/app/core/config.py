from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Bilingual DocQA API"
    environment: str = "local"
    debug: bool = False


settings = Settings()

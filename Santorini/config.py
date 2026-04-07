from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Santorini API"
    app_version: str = "1.0.0"
    app_description: str = "API do restaurante Santorini"
    debug: bool = False
    max_mesas: int = 20
    max_pessoas_por_mesa: int = 10

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

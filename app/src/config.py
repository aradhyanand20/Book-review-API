from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# # go to project root
# BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file= ".env",
        extra= "ignore"
    )

config = Settings()
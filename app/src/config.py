from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# # go to project root
# BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    REDIS_HOST : str = "Localhost"
    REDIS_PORT :int= 6379

    model_config = SettingsConfigDict(
        env_file= ".env",
        extra= "ignore"
    )

config = Settings()
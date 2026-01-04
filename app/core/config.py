from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = "AI Knowledge Orchestrator"
    API_V1_PREFIX: str = "/v1"
    ENV: str = os.getenv("ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

settings = Settings()

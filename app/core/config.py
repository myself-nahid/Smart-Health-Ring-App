import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "BISO AI Microservice"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME: str = "gpt-4-turbo" # or gpt-3.5-turbo for speed/cost

    class Config:
        env_file = ".env"

settings = Settings()
from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: Literal["prod", "test"]
    DB_HOST: str = "http://dynamodb:8000"
    AWS_REGION: str = "eu-central-1"


settings = Settings()

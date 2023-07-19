import boto3
import botocore.client

from periodic_lambda_app.config import settings
from periodic_lambda_app.repositories.base import TodoRepository
from periodic_lambda_app.repositories.dynamodb import DynamoDBTodoRepository
from periodic_lambda_app.repositories.in_memory import InMemoryTodoRepository


def make_dynamodb_client() -> botocore.client.BaseClient:
    return boto3.client(
        "dynamodb",
        endpoint_url=settings.DB_HOST,
        region_name=settings.AWS_REGION
    )


def get_todo_repository() -> TodoRepository:
    if settings.ENVIRONMENT == "test":
        return InMemoryTodoRepository()
    elif settings.ENVIRONMENT == "prod":
        client = make_dynamodb_client()
        return DynamoDBTodoRepository(client=client)
    raise RuntimeError("Unable to tell which repo to use.")

from uuid import UUID

from botocore.client import BaseClient
from botocore.exceptions import ClientError

from periodic_lambda_app.repositories.base import TodoRepository
from periodic_lambda_app.schemas import Todo


class DynamoDBTodoRepository(TodoRepository):
    """Implements TodoRepository using AWS DynamoDB."""

    def __init__(self, client: BaseClient) -> None:
        """Initializes the repository.

        Args:
            client: DynamoDB client.
        """
        self._client = client

    def create(self, todo: Todo) -> None:
        print(todo.dict())
        self._client.put_item(
            TableName="Todos",
            Item=todo.dict(),
        )
        return

    def list(self) -> list[Todo]:
        todos = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs['ExclusiveStartKey'] = start_key
                response = self._client.scan(TableName="Todos", **scan_kwargs)
                todos.extend(response.get('Items', []))
                start_key = response.get('LastEvaluatedKey', None)
                done = start_key is None
        except ClientError as err:
            raise RuntimeError from err
        return todos

    def save(self, to_change: Todo) -> Todo:
        pass

    def delete(self, todo_id: UUID) -> None:
        pass

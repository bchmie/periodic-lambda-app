from abc import ABC, abstractmethod
from uuid import UUID

from periodic_lambda_app.schemas import TodoCreate, Todo


class TodoRepository(ABC):
    @classmethod
    @abstractmethod
    def create(cls, todo: TodoCreate) -> Todo:
        ...

    @classmethod
    @abstractmethod
    def list(cls) -> list[Todo]:
        ...

    @classmethod
    @abstractmethod
    def save(cls, to_change: Todo) -> Todo:
        ...

    @classmethod
    @abstractmethod
    def delete(cls, todo_id: UUID) -> None:
        ...

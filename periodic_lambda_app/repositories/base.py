from abc import ABC, abstractmethod
from uuid import UUID

from periodic_lambda_app.schemas import Todo


class TodoRepository(ABC):
    @abstractmethod
    def create(self, todo: Todo) -> None:
        ...

    @abstractmethod
    def list(self) -> list[Todo]:
        ...

    @abstractmethod
    def save(self, to_change: Todo) -> Todo:
        ...

    @abstractmethod
    def delete(self, todo_id: UUID) -> None:
        ...

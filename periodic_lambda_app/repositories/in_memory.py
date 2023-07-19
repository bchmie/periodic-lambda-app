import copy
from datetime import datetime
from typing import Iterable
from uuid import UUID

from periodic_lambda_app.repositories.base import TodoRepository
from periodic_lambda_app.schemas import Todo


_todos = []


class InMemoryTodoRepository(TodoRepository):

    def create(self, todo: Todo) -> None:
        _todos.append(todo)

    def list(self) -> list[Todo]:
        return copy.deepcopy(_todos)

    def save(self, to_change: Todo) -> Todo:
        todo = next(todo for todo in _todos if todo.id == to_change.id)
        todo.status = to_change.status
        todo.inactive_since = to_change.inactive_since
        return copy.deepcopy(todo)

    def delete(self, todo_id: UUID) -> None:
        global _todos
        to_delete = next(todo for todo in _todos if todo.id == todo_id)
        if not to_delete:
            raise RuntimeError("Could not find TODO to delete")
        _todos = [todo for todo in _todos if todo.id != todo_id]

    def set_todos(self, todos: Iterable[Todo]) -> None:
        global _todos
        _todos = copy.deepcopy(todos)


starting_todos = [
    Todo(text="Do the laundry"),
    Todo(
        text="Feed the dog",
        created=datetime.now(),
        status="completed",
        inactive_since=datetime.now(),
    ),
    Todo(
        text="Take out the trash",
        created=datetime.now(),
        status="expired",
        inactive_since=datetime.now(),
    ),
]

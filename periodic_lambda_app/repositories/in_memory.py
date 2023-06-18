import copy
from datetime import datetime
from typing import Iterable
from uuid import UUID

from periodic_lambda_app.repositories.base import TodoRepository
from periodic_lambda_app.schemas import Todo, TodoCreate


class InMemoryTodoRepository(TodoRepository):
    _todos = []

    @classmethod
    def create(cls, todo: TodoCreate) -> Todo:
        new_todo = Todo(text=todo.text)
        cls._todos.append(new_todo)
        return new_todo

    @classmethod
    def list(cls) -> list[Todo]:
        return copy.deepcopy(cls._todos)

    @classmethod
    def save(cls, to_change: Todo) -> Todo:
        todo = next(todo for todo in cls._todos if todo.id == to_change.id)
        todo.status = to_change.status
        todo.inactive_since = to_change.inactive_since
        return copy.deepcopy(todo)

    @classmethod
    def delete(cls, todo_id: UUID) -> None:
        to_delete = next(todo for todo in cls._todos if todo.id == todo_id)
        if not to_delete:
            raise RuntimeError("Could not find TODO to delete")
        cls._todos = [todo for todo in cls._todos if todo.id != todo_id]

    @classmethod
    def set_todos(cls, todos: Iterable[Todo]) -> None:
        cls._todos = copy.deepcopy(todos)


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

InMemoryTodoRepository.set_todos(starting_todos)

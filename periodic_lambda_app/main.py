from datetime import datetime
from operator import attrgetter
from uuid import UUID

from fastapi import FastAPI
from starlette import status
from starlette.responses import FileResponse

from periodic_lambda_app.schemas import Todo, TodoCreate

app = FastAPI()

todos = [
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


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("periodic_lambda_app/static/index.html")


@app.get("/todo/", status_code=status.HTTP_200_OK, response_model=list[Todo])
async def list_todo() -> list[Todo]:
    return sorted(todos, key=attrgetter("text"))


@app.post("/todo/", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(todo: TodoCreate) -> Todo:
    new_todo = Todo(text=todo.text)
    todos.append(new_todo)
    return new_todo


@app.put("/todo/{id}/", status_code=status.HTTP_200_OK, response_model=Todo)
async def complete_todo(id: UUID, todo: Todo) -> Todo:
    current = next(todo for todo in todos if todo.id == id)
    current.status = "completed"
    current.inactive_since = datetime.now()
    return current


@app.delete("/todo/{id}/", status_code=status.HTTP_200_OK)
async def delete_todo(id: UUID) -> None:
    global todos
    todos = [todo for todo in todos if todo.id != id]
    return

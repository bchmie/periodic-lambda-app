from contextlib import asynccontextmanager
from datetime import datetime
from operator import attrgetter
from uuid import UUID

from fastapi import FastAPI, HTTPException, Depends
from mangum import Mangum
from starlette import status
from starlette.responses import FileResponse

from periodic_lambda_app.config import settings
from periodic_lambda_app.dependencies import get_todo_repository
from periodic_lambda_app.repositories.base import TodoRepository
from periodic_lambda_app.repositories.in_memory import starting_todos, InMemoryTodoRepository
from periodic_lambda_app.schemas import Todo, TodoCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.ENVIRONMENT == "test":
        InMemoryTodoRepository().set_todos(starting_todos)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("periodic_lambda_app/static/index.html")


@app.get("/todo", status_code=status.HTTP_200_OK, response_model=list[Todo])
async def list_todo(todo_repository: TodoRepository = Depends(get_todo_repository)) -> list[Todo]:
    return sorted(todo_repository.list(), key=attrgetter("text"))


@app.post("/todo", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(todo: TodoCreate, todo_repository: TodoRepository = Depends(get_todo_repository)) -> Todo:
    new_todo = Todo(text=todo.text)
    todo_repository.create(new_todo)
    return new_todo


@app.put("/todo/{id}", status_code=status.HTTP_200_OK, response_model=Todo)
async def complete_todo(id: UUID, todo: Todo, todo_repository: TodoRepository = Depends(get_todo_repository)) -> Todo:
    todo.inactive_since = datetime.now()
    modified = todo_repository.save(todo)
    return modified


@app.delete("/todo/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(id: UUID, todo_repository: TodoRepository = Depends(get_todo_repository)) -> None:
    try:
        todo_repository.delete(todo_id=id)
    except RuntimeError:
        raise HTTPException(status_code=404, detail="Todo not found")
    return


handler = Mangum(app, lifespan="off")

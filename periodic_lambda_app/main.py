from datetime import datetime
from operator import attrgetter
from uuid import UUID

from fastapi import FastAPI, HTTPException
from mangum import Mangum
from starlette import status
from starlette.responses import FileResponse

from periodic_lambda_app.repositories.in_memory import InMemoryTodoRepository
from periodic_lambda_app.schemas import Todo, TodoCreate

app = FastAPI()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("periodic_lambda_app/static/index.html")


@app.get("/todo", status_code=status.HTTP_200_OK, response_model=list[Todo])
async def list_todo() -> list[Todo]:
    return sorted(InMemoryTodoRepository.list(), key=attrgetter("text"))


@app.post("/todo", status_code=status.HTTP_201_CREATED, response_model=Todo)
async def create_todo(todo: TodoCreate) -> Todo:
    new_todo = InMemoryTodoRepository.create(todo)
    return new_todo


@app.put("/todo/{id}", status_code=status.HTTP_200_OK, response_model=Todo)
async def complete_todo(id: UUID, todo: Todo) -> Todo:
    todo.inactive_since = datetime.now()
    modified = InMemoryTodoRepository.save(todo)
    return modified


@app.delete("/todo/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(id: UUID) -> None:
    try:
        InMemoryTodoRepository.delete(todo_id=id)
    except RuntimeError:
        raise HTTPException(status_code=404, detail="Todo not found")
    return


handler = Mangum(app, lifespan="off")

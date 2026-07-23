from fastapi import APIRouter, HTTPException

from app.schemas.todos import (
    Todo, 
    TodosCreate,
    TodosUpdate
)
from app.todos_logic import all_todos

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.get('/{todo_id}', response_model=Todo)
def get_todo(todo_id: int):
    for todo in all_todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.get("/")
def get_todos(first_n: int = None):
    if first_n:
        return {"result": all_todos[:first_n]}
    return {"result": all_todos}

@router.post("/", response_model=Todo)
def create_todo(new_todo: TodosCreate):
    idx = len(all_todos)
    created_todo = Todo(id=idx, todo_name=new_todo.todo_name,
        todo_description=new_todo.todo_description, priority=new_todo.priority)
    all_todos.append(created_todo)
    return created_todo

@router.put("/{todo_id}")
def update_todo(todo_id: int, new_todo: TodosUpdate):
    for todo in all_todos:
        if todo.id == todo_id:
            if new_todo.todo_name:
                todo.todo_name = new_todo.todo_name
            if new_todo.todo_description:
                todo.todo_description = new_todo.todo_description
            if new_todo.priority:
                todo.priority = new_todo.priority 
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/{todo_id}")
def delete_todo(todo_id: int):
    for i in range(len(all_todos)):
        if all_todos[i].id == todo_id:
            all_todos.pop(i)
            return {"result": all_todos}
    raise HTTPException(status_code=404, detail="Todo not found")
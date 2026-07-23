from enum import IntEnum
from typing import Optional, List
from pydantic import BaseModel, Field

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class TodosBase(BaseModel):
    todo_name: str = Field(..., max_length=255, description="Name of the todo")
    todo_description: str = Field(..., max_length=255, description="Description of the todo")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")

class Todo(TodosBase):
    id: int = Field(..., description="id of the todo")

class TodosCreate(TodosBase):
    pass

class TodosUpdate(BaseModel):
    todo_name: Optional[str] = Field(default=None, max_length=255, description="Name of the todo")
    todo_description: Optional[str] = Field(default=None, description="Description of the todo")
    priority: Optional[Priority] = Field(default=None, description="Priority of the todo")
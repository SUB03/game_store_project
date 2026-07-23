from app.schemas.todos import Todo, TodosCreate, TodosUpdate, Priority


all_todos = [
    Todo(id=0, todo_name="do something", 
        todo_description="just do something", priority=Priority.HIGH),
    Todo(id=1, todo_name="break", 
        todo_description="just have a break", priority=Priority.LOW),
    Todo(id=2, todo_name="continue",
        todo_description="just continue doing something", priority=Priority.MEDIUM),
]
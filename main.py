from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Todo, TodoModel
from database import engine, get_db

Todo.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello world" }

@app.get("/todos")
async def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return { "todos": todos }

@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        return { "todo": db_todo }
    else:
        raise HTTPException(status_code=404, detail="No todo found")

@app.post("/todos")
async def create_todo(todo: TodoModel, db: Session = Depends(get_db)):
    db_todo = Todo(id=todo.id, item=todo.item)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return { "message": "Todo has been added" }

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo_obj: TodoModel, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db_todo.item = todo_obj.item
        db.commit()
        db.refresh(db_todo)
        return { "todo": db_todo }
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return { "message": "Todo has been deleted" }
    else:
        raise HTTPException(status_code=404, detail="Todo not found")
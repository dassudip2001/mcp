from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_mcp import FastApiMCP
import database
import models
import schemas

app = FastAPI(title="FastAPI Todo App")

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/todos/", response_model=list[schemas.Todo],operation_id="get_todos")
def list_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()


@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, updates: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).get(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@app.get("/")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    mcp = FastApiMCP(app,
                   include_operations=["get_todos"]  )
    mcp.mount()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


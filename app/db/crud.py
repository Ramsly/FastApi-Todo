from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

from .models import Todo


def create_todo(db: Session, content: str) -> Todo:
    db_todo = Todo(content=content)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session) -> list[Todo]:
    return db.query(Todo).all()


def get_todo_by_id(db: Session, todo_id: int) -> Todo | None:
    return db.query(Todo).where(Todo.id == todo_id).first()


def toggle_is_done(db: Session, todo_id: int) -> Todo | None:
    db_todo = get_todo_by_id(db, todo_id)
    if not db_todo:
        raise HTTPException(
            detail='Item was not found',
            status_code=404
        )
    db_todo.is_done = not db_todo.is_done
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, content: str) -> Todo | None:
    db_todo = get_todo_by_id(db, todo_id)
    if not db_todo:
        raise HTTPException(
            detail='Item was not found',
            status_code=404
        )
    db_todo.content = content
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete(db: Session, todo_id: int) -> None:
    db_todo = get_todo_by_id(db, todo_id)
    if not db_todo:
        raise HTTPException(
            detail='Item was not found',
            status_code=404
        )
    db.delete(db_todo)
    db.commit()
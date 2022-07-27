from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .depends import get_db
from .schemas.request import DataForTodoScheme
from .schemas.response import TodoResponseScheme
from .crud import get_todos, create_todo, get_todo_by_id, delete, toggle_is_done, update_todo
from .database import Base, engine

Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/todo",
    tags=['Todo']
)


@router.post('/create', response_model=TodoResponseScheme)
async def create_one_todo(data: DataForTodoScheme, db: Session = Depends(get_db)):
    return create_todo(db, content=data.content)


@router.get('/all', response_model=list[TodoResponseScheme])
async def get_all_todos(db: Session = Depends(get_db)):
    return get_todos(db)


@router.get('/get/{id}', response_model=TodoResponseScheme)
async def get_todo(id: int, db: Session = Depends(get_db)):
    todo = get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(
            detail='Item was not found',
            status_code=404
        )
    return todo


@router.put('/is_done/{id}', response_model=TodoResponseScheme)
async def todo_is_done(id: int, db: Session = Depends(get_db)):
    return toggle_is_done(db, id)


@router.put('/change_content', response_model=TodoResponseScheme)
async def change_content(id: int, content: str, db: Session = Depends(get_db)):
    return update_todo(db, todo_id=id, content=content)


@router.delete('/delete/{id}')
async def delete_todo(id: int, db: Session = Depends(get_db)):
    return delete(db, id)
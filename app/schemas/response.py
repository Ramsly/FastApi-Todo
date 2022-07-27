from pydantic import BaseModel

from datetime import datetime


class TodoResponseScheme(BaseModel):
    id: int
    content: str
    is_done: bool | None = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True
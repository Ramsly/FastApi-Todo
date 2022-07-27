from pydantic import BaseModel


class DataForTodoScheme(BaseModel):
    content: str
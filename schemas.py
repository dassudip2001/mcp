from pydantic import BaseModel
class TodoBase(BaseModel):
    title: str
    description: str|None = None


class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    title: str|None = None
    description: str|None = None
    completed: bool|None = None

class Todo(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
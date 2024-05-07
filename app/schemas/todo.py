from pydantic import BaseModel


# ToDo model
class ToDo(BaseModel):
    title: str
    description: str

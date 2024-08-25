from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)

    def __init__(self, id, item):
        self.id = id
        self.item = item

    def __repr__(self):
        return f"{self.item}"
    
class TodoModel(BaseModel):
    id: int
    item: str
    
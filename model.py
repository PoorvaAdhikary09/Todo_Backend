from pydantic import BaseModel
from datetime import date
from typing import Optional

class Task(BaseModel):
    slno: int
    title: str
    due_date: date
    completed: bool = False

class UpdateTask(BaseModel):
    title: Optional[str] = None
    due_date: Optional[date] = None
    completed: Optional[bool] = None

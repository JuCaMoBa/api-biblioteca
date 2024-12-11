from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    ISBN: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: int
    ISBN: str

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    ISBN: Optional[str] = None


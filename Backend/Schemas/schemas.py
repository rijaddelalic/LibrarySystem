from pydantic import BaseModel
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookOut(BookBase):
    id: int
    image_filename: str | None = None
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    membershipId: str | None = None

class UserOut(BaseModel):
    id: int
    name: str
    lastname: str
    email: str
    membershipId: str
    profile_image: str | None = None
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class LoanCreate(BaseModel):
    user_id: int
    book_id: int

class LoanOut(LoanCreate):
    id: int
    timestamp: datetime | None = None
    return_date: datetime | None = None
    class Config:
        from_attributes = True
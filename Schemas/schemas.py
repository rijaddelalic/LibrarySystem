from pydantic import BaseModel
from datetime import date

# USER
class UserBase(BaseModel):
    name: str
    lastname: str
    membershipId: str

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

# BOOK
class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookCreate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    class Config:
        orm_mode = True

# LOAN
class LoanBase(BaseModel):
    user_id: int
    book_id: int
    return_date: date | None = None   # NOVO polje

class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    # NEMA return_date u kreiranju!

class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    return_date: date | None = None

    class Config:
        orm_mode = True

class LoanCreate(BaseModel):
    user_id: int
    book_id: int

    class Config:
        extra = "forbid"  # odbija polja koja nisu definisana

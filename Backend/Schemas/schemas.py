from pydantic import BaseModel
from datetime import datetime

# --- BOOK SCHEMAS ---
class BookBase(BaseModel):
    title: str
    author: str
    year: int

class BookOut(BookBase):
    id: int
    image_filename: str | None = None

    class Config:
        from_attributes = True

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str
    lastname: str
    membershipId: str
    email: str  # PROMIJENIO SAM 'mail' u 'email' da se poklapa sa JS-om

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    # UserOut NE nasljeđuje UserCreate da ne bi slao lozinku nazad!

    class Config:
        from_attributes = True

# --- LOAN SCHEMAS ---
class LoanCreate(BaseModel):
    user_id: int
    book_id: int

class LoanOut(LoanCreate):
    id: int
    timestamp: datetime | None = None
    return_date: datetime | None = None

    class Config:
        from_attributes = True
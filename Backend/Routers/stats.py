from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
# ISPRAVLJENI IMPORTI:
from Models.User import User
from Models.Book import Book
from Models.Loan import Loan

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    users_count = db.query(User).count()
    books_count = db.query(Book).count()
    loans_count = db.query(Loan).count()
    return {
        "users": users_count,
        "books": books_count,
        "loans": loans_count
    }
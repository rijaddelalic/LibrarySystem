from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from models import Loan, User, Book

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/")
def loan_book(user_id: int, book_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()
    if not user or not book:
        raise HTTPException(status_code=404, detail="User or Book not found")
    if db.query(Loan).filter(Loan.user_id == user_id, Loan.book_id == book_id).first():
        raise HTTPException(status_code=400, detail="Book already loaned to this user")
    loan = Loan(user_id=user_id, book_id=book_id)
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

@router.get("/")
def list_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()

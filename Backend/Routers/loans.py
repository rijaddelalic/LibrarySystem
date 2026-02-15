from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from Models.Loan import Loan  # Pazi na veliko L
from Models.User import User
from Models.Book import Book
from db.connection import get_db
from Schemas.schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanOut)
def loan_book(loan: LoanCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == loan.user_id).first()
    book = db.query(Book).filter(Book.id == loan.book_id).first()

    if not user or not book:
        raise HTTPException(status_code=404, detail="Korisnik ili Knjiga nisu pronađeni")

    new_loan = Loan(
        user_id=loan.user_id,
        book_id=loan.book_id,
        timestamp=datetime.now()
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan

@router.get("/", response_model=list[LoanOut])
def list_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()

@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Posudba nije pronađena")
    db.delete(loan)
    db.commit()
    return {"message": "Deleted"}
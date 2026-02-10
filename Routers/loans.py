from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from models import Loan, User, Book
from db.connection import get_db
from Schemas.schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/loans", tags=["loans"])

# CREATE - posudba knjige
@router.post("/", response_model=LoanOut)
def loan_book(loan: LoanCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == loan.user_id).first()
    book = db.query(Book).filter(Book.id == loan.book_id).first()

    if not user or not book:
        raise HTTPException(status_code=404, detail="User or Book not found")

    # Provjera da li je knjiga već posuđena (aktivna posudba bez return_date)
    if db.query(Loan).filter(Loan.book_id == loan.book_id, Loan.return_date == None).first():
        raise HTTPException(status_code=400, detail="Book is already loaned")

    # Provjera max 3 knjige po korisniku
    active_loans = db.query(Loan).filter(Loan.user_id == loan.user_id, Loan.return_date == None).count()
    if active_loans >= 3:
        raise HTTPException(status_code=400, detail="User already has 3 books loaned")

    # EKSPPLICITNO postavi return_date=None
    new_loan = Loan(user_id=loan.user_id, book_id=loan.book_id, return_date=None)
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan

# READ - sve posudbe
@router.get("/", response_model=list[LoanOut])
def list_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()

# READ - posudbe jednog korisnika
@router.get("/user/{user_id}", response_model=list[LoanOut])
def user_loans(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return db.query(Loan).filter(Loan.user_id == user_id).all()

# DELETE - brisanje posudbe
@router.delete("/{loan_id}")
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    db.delete(loan)
    db.commit()
    return {"message": "Loan deleted successfully"}

# RETURN - vraćanje knjige
@router.put("/{loan_id}/return", response_model=LoanOut)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    loan.return_date = date.today()
    db.commit()
    db.refresh(loan)
    return loan

# EXTRA - aktivne posudbe (bez return_date)
@router.get("/active", response_model=list[LoanOut])
def active_loans(db: Session = Depends(get_db)):
    return db.query(Loan).filter(Loan.return_date == None).all()
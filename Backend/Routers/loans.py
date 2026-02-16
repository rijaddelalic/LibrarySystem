from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from Models.Loan import Loan
from db.connection import get_db
from Schemas.schemas import LoanCreate, LoanOut

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanOut)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    new_l = Loan(user_id=loan.user_id, book_id=loan.book_id, timestamp=datetime.now())
    db.add(new_l); db.commit(); db.refresh(new_l)
    return new_l

@router.get("/", response_model=list[LoanOut])
def active_loans(db: Session = Depends(get_db)):
    return db.query(Loan).filter(Loan.return_date == None).all()

@router.get("/history", response_model=list[LoanOut])
def loan_history(db: Session = Depends(get_db)):
    return db.query(Loan).all()

@router.delete("/{loan_id}")
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    loan.return_date = datetime.now() # Ne brišemo, samo stavljamo datum povratka
    db.commit()
    return {"msg": "returned"}
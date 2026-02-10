from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Book, Loan
from db.connection import get_db
from Schemas.schemas import BookCreate, BookOut

router = APIRouter(prefix="/books", tags=["books"])

# CREATE
@router.post("/", response_model=BookOut)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# READ
@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

# UPDATE
@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# DELETE
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}

# AVAILABILITY
@router.get("/{book_id}/availability")
def check_availability(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    loan = db.query(Loan).filter(Loan.book_id == book_id).first()
    return {"book_id": book_id, "available": loan is None}
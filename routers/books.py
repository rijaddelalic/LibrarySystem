from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from models import Book

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/")
def add_book(title: str, author: str, year: int, db: Session = Depends(get_db)):
    if db.query(Book).filter(Book.title == title, Book.author == author).first():
        raise HTTPException(status_code=400, detail="Book already exists")
    new_book = Book(title=title, author=author, year=year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/")
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

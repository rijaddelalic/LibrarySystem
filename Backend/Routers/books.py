import shutil
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from Models.Book import Book # ISPRAVLJENA PUTANJA
from db.connection import get_db
from Schemas.schemas import BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookOut)
def add_book(
        title: str = Form(...),
        author: str = Form(...),
        year: int = Form(...),
        image: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    path_for_db = None
    if image:
        # Spasavamo sliku u static/images
        filename = f"static/images/{image.filename}"
        with open(filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        path_for_db = filename

    new_book = Book(title=title, author=author, year=year, image_filename=path_for_db)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book: raise HTTPException(status_code=404)
    if book.image_filename and os.path.exists(book.image_filename):
        os.remove(book.image_filename)
    db.delete(book)
    db.commit()
    return {"message": "Deleted"}
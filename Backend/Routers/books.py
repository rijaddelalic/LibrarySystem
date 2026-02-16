import shutil, os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from Models.Book import Book
from db.connection import get_db
from Schemas.schemas import BookOut

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookOut)
def add_book(title: str = Form(...), author: str = Form(...), year: int = Form(...),
             image: UploadFile = File(None), db: Session = Depends(get_db)):

    exist = db.query(Book).filter(Book.title == title, Book.author == author).first()
    if exist: raise HTTPException(status_code=400, detail="Knjiga već postoji!")

    path = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        path = f"static/images/b_{image.filename}"
        with open(path, "wb") as buf:
            shutil.copyfileobj(image.file, buf)

    new_b = Book(title=title, author=author, year=year, image_filename=path)
    db.add(new_b); db.commit(); db.refresh(new_b)
    return new_b

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    b = db.query(Book).filter(Book.id == book_id).first()
    if b:
        db.delete(b); db.commit()
    return {"msg": "ok"}
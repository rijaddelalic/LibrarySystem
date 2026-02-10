from fastapi import FastAPI, HTTPException
from Services.LibraryService import LibraryService
from Models.Book import Book
from Core.Exceptions import (
    UserNotFoundError, UserAlreadyExistsError,
    BookNotFoundError, BookAlreadyExistsError,
    AlreadyBorrowedError, NotBorrowedError, AlreadyReturnedError
)

app = FastAPI(title="Library System API")
service = LibraryService()

@app.post("/users")
def add_user(name: str, lastname: str, membershipId: str):
    try:
        service.add_user(name, lastname, membershipId)
        return {"message": "User added successfully"}
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/books")
def add_book(title: str, author: str, year: int):
    try:
        service.add_book(Book(title=title, author=author, year=year))
        return {"message": "Book added successfully"}
    except BookAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/borrow")
def borrow_book(membershipId: str, book_title: str):
    try:
        service.borrow_book(membershipId, book_title)
        return {"message": "Book borrowed successfully"}
    except (UserNotFoundError, BookNotFoundError, AlreadyBorrowedError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/return")
def return_book(membershipId: str, book_title: str):
    try:
        service.return_book(membershipId, book_title)
        return {"message": "Book returned successfully"}
    except (NotBorrowedError, AlreadyReturnedError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions")
def list_transactions():
    return service.list_transactions()

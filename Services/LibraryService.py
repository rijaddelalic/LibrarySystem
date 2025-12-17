from Models.Book import Book
from db import book_dao, user_dao, transaction_dao
from Core.Exceptions import (
    UserNotFoundError, UserAlreadyExistsError,
    BookNotFoundError, BookAlreadyExistsError,
    AlreadyBorrowedError, NotBorrowedError, AlreadyReturnedError
)

class LibraryService:
    def add_book(self, book: Book) -> None:
        existing = [b for b in book_dao.get_books() if b.title == book.title and b.author == book.author]
        if existing:
            raise BookAlreadyExistsError(f"Knjiga '{book.title}' već postoji u bazi.")
        book_dao.create_book(book.title, book.author, book.year)

    def list_books(self):
        return book_dao.get_books()

    def add_user(self, name: str, lastname: str, membershipId: str) -> None:
        existing = [u for u in user_dao.get_users() if u.membershipId == membershipId]
        if existing:
            raise UserAlreadyExistsError(f"Korisnik sa ID '{membershipId}' već postoji.")
        user_dao.create_user(name, lastname, membershipId)

    def list_users(self):
        return user_dao.get_users()

    def borrow_book(self, membershipId: str, book_title: str) -> None:
        user = next((u for u in user_dao.get_users() if u.membershipId == membershipId), None)
        if not user:
            raise UserNotFoundError(f"Korisnik sa ID '{membershipId}' ne postoji.")

        book = next((b for b in book_dao.get_books() if b.title == book_title), None)
        if not book:
            raise BookNotFoundError(f"Knjiga '{book_title}' ne postoji u bazi.")

        transactions = transaction_dao.get_transactions()
        active_borrow = next(
            (t for t in transactions if t.book_title == book_title and t.action == "borrow"
             and not any(r for r in transactions if r.book_title == book_title and r.user_id == t.user_id and r.action == "return")),
            None
        )
        if active_borrow:
            raise AlreadyBorrowedError(f"Knjiga '{book_title}' je već posuđena i nije vraćena.")

        transaction_dao.create_transaction(membershipId, book_title, "borrow")

    def return_book(self, membershipId: str, book_title: str) -> None:
        transactions = transaction_dao.get_transactions()

        borrowed = next((t for t in transactions if t.book_title == book_title and t.user_id == membershipId and t.action == "borrow"), None)
        returned = next((t for t in transactions if t.book_title == book_title and t.user_id == membershipId and t.action == "return"), None)

        if not borrowed:
            raise NotBorrowedError(f"Korisnik '{membershipId}' nije posudio knjigu '{book_title}'.")

        if returned:
            raise AlreadyReturnedError(f"Knjiga '{book_title}' je već vraćena od strane korisnika '{membershipId}'.")

        transaction_dao.create_transaction(membershipId, book_title, "return")

    def list_transactions(self):
        return transaction_dao.get_transactions()

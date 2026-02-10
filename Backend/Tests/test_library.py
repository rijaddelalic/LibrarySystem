import pytest
from Models.Book import Book
from Services.LibraryService import LibraryService
from db import book_dao, user_dao, transaction_dao
from Core.Exceptions import (
    UserNotFoundError, UserAlreadyExistsError,
    BookNotFoundError, BookAlreadyExistsError,
    AlreadyBorrowedError, NotBorrowedError, AlreadyReturnedError
)

@pytest.fixture
def service():
    # reset baze prije svakog testa
    session = transaction_dao.get_session()
    session.query(transaction_dao.TransactionORM).delete()
    session.query(user_dao.UserORM).delete()
    session.query(book_dao.BookORM).delete()
    session.commit()
    session.close()
    return LibraryService()

def test_add_user_duplicate(service):
    service.add_user("Rijad", "Test", "U1")
    with pytest.raises(UserAlreadyExistsError):
        service.add_user("Rijad", "Test", "U1")

def test_add_book_duplicate(service):
    service.add_book(Book(title="BookX", author="Author", year=2020))
    with pytest.raises(BookAlreadyExistsError):
        service.add_book(Book(title="BookX", author="Author", year=2020))

def test_borrow_nonexistent_user(service):
    service.add_book(Book(title="BookY", author="Author", year=2020))
    with pytest.raises(UserNotFoundError):
        service.borrow_book("U999", "BookY")

def test_borrow_nonexistent_book(service):
    service.add_user("Rijad", "Test", "U1")
    with pytest.raises(BookNotFoundError):
        service.borrow_book("U1", "DoesNotExist")

def test_cannot_borrow_same_book_twice(service):
    service.add_user("Rijad", "Test", "U1")
    service.add_book(Book(title="BookZ", author="Author", year=2020))
    service.borrow_book("U1", "BookZ")
    with pytest.raises(AlreadyBorrowedError):
        service.borrow_book("U1", "BookZ")

def test_cannot_return_book_not_borrowed(service):
    service.add_user("Rijad", "Test", "U1")
    service.add_book(Book(title="BookA", author="Author", year=2020))
    with pytest.raises(NotBorrowedError):
        service.return_book("U1", "BookA")

def test_cannot_return_book_twice(service):
    service.add_user("Rijad", "Test", "U1")
    service.add_book(Book(title="BookB", author="Author", year=2020))
    service.borrow_book("U1", "BookB")
    service.return_book("U1", "BookB")
    with pytest.raises(AlreadyReturnedError):
        service.return_book("U1", "BookB")

def test_two_users_same_book(service):
    service.add_user("Rijad", "Test", "U1")
    service.add_user("Amir", "Test", "U2")
    service.add_book(Book(title="BookC", author="Author", year=2020))

    service.borrow_book("U1", "BookC")
    with pytest.raises(AlreadyBorrowedError):
        service.borrow_book("U2", "BookC")

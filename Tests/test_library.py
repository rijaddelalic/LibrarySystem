from db.book_dao import create_book, get_books
from db.user_dao import create_user, get_users
from db.transaction_dao import create_transaction, get_transactions

def test_add_book():
    create_book("Test Book", "Test Author", 2025)
    books = get_books()
    assert any(b.title == "Test Book" for b in books)

def test_add_user():
    create_user("Test", "User", "T001")
    users = get_users()
    assert any(u.membershipId == "T001" for u in users)

def test_transaction():
    create_transaction("T001", "Test Book", "borrow")
    transactions = get_transactions()
    assert any(t.action == "borrow" and t.book_title == "Test Book" for t in transactions)
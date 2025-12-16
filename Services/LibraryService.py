from Models.Book import Book
from db import book_dao, user_dao, transaction_dao

class LibraryService:
    def add_book(self, book: Book) -> None:
        # Provjera da li knjiga već postoji
        existing = [b for b in book_dao.get_books() if b.title == book.title and b.author == book.author]
        if existing:
            print(f"⚠️ Knjiga '{book.title}' već postoji u bazi.")
            return
        book_dao.create_book(book.title, book.author, book.year)

    def list_books(self):
        return book_dao.get_books()

    def add_user(self, name: str, lastname: str, membershipId: str) -> None:
        # Provjera da li korisnik već postoji
        existing = [u for u in user_dao.get_users() if u.membershipId == membershipId]
        if existing:
            print(f"⚠️ Korisnik sa ID '{membershipId}' već postoji.")
            return
        user_dao.create_user(name, lastname, membershipId)

    def list_users(self):
        return user_dao.get_users()

    def borrow_book(self, membershipId: str, book_title: str) -> None:
        # Provjeri da li korisnik postoji
        user = next((u for u in user_dao.get_users() if u.membershipId == membershipId), None)
        if not user:
            print(f"❌ Korisnik sa ID '{membershipId}' ne postoji.")
            return

        # Provjeri da li knjiga postoji
        book = next((b for b in book_dao.get_books() if b.title == book_title), None)
        if not book:
            print(f"❌ Knjiga '{book_title}' ne postoji u bazi.")
            return

        # Provjeri da li je knjiga već posuđena
        transactions = transaction_dao.get_transactions()
        borrowed = next((t for t in transactions if t.book_title == book_title and t.action == "borrow"), None)
        returned = next((t for t in transactions if t.book_title == book_title and t.action == "return"), None)

        if borrowed and not returned:
            print(f"⚠️ Knjiga '{book_title}' je već posuđena i nije vraćena.")
            return

        transaction_dao.create_transaction(membershipId, book_title, "borrow")

    def return_book(self, membershipId: str, book_title: str) -> None:
        # Provjeri da li postoji transakcija posudbe
        transactions = transaction_dao.get_transactions()
        borrowed = next((t for t in transactions if t.book_title == book_title and t.user_id == membershipId and t.action == "borrow"), None)

        if not borrowed:
            print(f" Korisnik '{membershipId}' nije posudio knjigu '{book_title}', pa je ne može vratiti.")
            return

        transaction_dao.create_transaction(membershipId, book_title, "return")

    def list_transactions(self):
        return transaction_dao.get_transactions()
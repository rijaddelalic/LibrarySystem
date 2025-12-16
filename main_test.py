from Models.Book import Book
from Models.Library import Library
from Models.User import User
from Models.Transaction import Transaction
from Models.Librarian import Librarian

# Kreiraj biblioteku i bibliotekara
library = Library()
librarian = Librarian("Amir", "Hodžić")

# Dodaj knjige
librarian.addBook(library, Book("Na Drini ćuprija", "Ivo Andrić", 1945))
librarian.addBook(library, Book("Derviš i smrt", "Meša Selimović", 1966))

# Kreiraj korisnika
user = User("Rijad", "Kovačević", "CL001")

# Korisnik iznajmljuje knjigu
user.Loan_Book("Na Drini ćuprija")
transaction1 = Transaction(user_id=user.membershipId, book_title="Na Drini ćuprija", action="borrow")

print(transaction1)

# Korisnik vraća knjigu
user.Return_Book("Na Drini ćuprija")
transaction2 = Transaction(user_id=user.membershipId, book_title="Na Drini ćuprija", action="return")

print(transaction2)

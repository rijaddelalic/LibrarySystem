from db.connection import Base, engine
from Services.LibraryService import LibraryService
from Models.Book import Book

# Kreiraj tabele
Base.metadata.create_all(bind=engine)

service = LibraryService()

# 1. Dodaj knjigu
print("\n--- Dodavanje knjige ---")
service.add_book(Book("Na Drini ćuprija", "Ivo Andrić", 1945))

# 2. Pokušaj dodati istu knjigu ponovo (validacija će spriječiti duplikat)
service.add_book(Book("Na Drini ćuprija", "Ivo Andrić", 1945))

# 3. Dodaj korisnika
print("\n--- Dodavanje korisnika ---")
service.add_user("Rijad", "Kovačević", "CL001")

# 4. Pokušaj dodati istog korisnika ponovo (validacija će spriječiti duplikat)
service.add_user("Rijad", "Kovačević", "CL001")

# 5. Korisnik iznajmljuje knjigu
print("\n--- Posudba knjige ---")
service.borrow_book("CL001", "Na Drini ćuprija")

# 6. Pokušaj posuditi istu knjigu ponovo (validacija će spriječiti jer nije vraćena)
service.borrow_book("CL001", "Na Drini ćuprija")

# 7. Pokušaj vratiti knjigu koju korisnik nije posudio
print("\n--- Vraćanje knjige koju korisnik nije posudio ---")
service.return_book("CL001", "Derviš i smrt")

# 8. Ispravno vraćanje knjige
print("\n--- Ispravno vraćanje knjige ---")
service.return_book("CL001", "Na Drini ćuprija")

# 9. Ispis iz baze
print("\n📚 Knjige:")
for b in service.list_books():
    print(f"{b.title} - {b.author} ({b.year})")

print("\n👤 Korisnici:")
for u in service.list_users():
    print(f"{u.name} {u.lastname} (ID: {u.membershipId})")

print("\n🔄 Transakcije:")
for t in service.list_transactions():
    print(f"{t.action.upper()} - {t.book_title} (User: {t.user_id}, Time: {t.timestamp})")
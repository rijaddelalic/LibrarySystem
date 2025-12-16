from Models.Library import Library
from Models.Book import Book

class Librarian:
    def __init__(self,name:str,lastname:str)->None:
        self.name = name
        self.lastname = lastname

    def addBook(self,library:Library,book:Book)->None:
        library.addBook(book)

    def removeBook(self,library:Library,title:str)->None:
        library.removeBook(title)

    def __str__(self) -> str:
        return f"Librarian: {self.name} {self.lastname}"


from typing import List

from Models import Book


class Library:
    def __init__(self)->None:
        self.books: List[Book] = []
    def addBook(self, book: Book)->None:
        self.books.append(book)
    def removeBook(self, title: str) -> None:
        self.books = [book for book in self.books if book.title != title]
    def searchBookByAuthor(self,author:str)->List[Book]:
        return [b for b in self.books if b.author==author]
    def searchBookByTitle(self,title:str)->List[Book]:
        return [b for b in self.books if b.title==title]
    def printBooks(self)->None:
        for b in self.books:
            print(b)

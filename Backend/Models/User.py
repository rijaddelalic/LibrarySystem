from typing import List

class User:
    def __init__(self,name:str,lastname:str,membershipId:str)->None:
        self.name = name
        self.lastname = lastname
        self.membershipId = membershipId
        self.loaned_books:List[str] = []

    def Loan_Book(self,title:str)->None:
        self.loaned_books.append(title)

    def Return_Book(self,title:str)->None:
        if title in self.loaned_books:
            self.loaned_books.remove(title)


    def __str__(self)->str:
        return f"{self.name.upper()} {self.lastname.upper()} (ID: {self.membershipId})"


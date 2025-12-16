class Book:
    def __init__(self,title:str,author:str,year:int)->None:
        self.title = title
        self.author = author
        self.year = year

    def __str__(self)->str:
        return f"{self.title} by {self.author} on {self.year}"
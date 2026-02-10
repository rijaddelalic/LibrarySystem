from sqlalchemy import Column, Integer, String
from db.connection import Base, get_session

class BookORM(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

def create_book(title:str,author:str,year:int)->None:
    session = get_session()
    new_book = BookORM(title=title,author=author,year=year)
    session.add(new_book)
    session.commit()
    session.close()

def get_books():
    session = get_session()
    books = session.query(BookORM).all()
    session.close()
    return books



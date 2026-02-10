from sqlalchemy import Column, Integer, String
from db.connection import Base, get_session

class LibrarianORM(Base):
    __tablename__ = "librarians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

def create_librarian(name: str, lastname: str) -> None:
    session = get_session()
    new_librarian = LibrarianORM(name=name, lastname=lastname)
    session.add(new_librarian)
    session.commit()
    session.close()

def get_librarians():
    session = get_session()
    librarians = session.query(LibrarianORM).all()
    session.close()
    return librarians
from sqlalchemy import Column, Integer, String
from db.connection import Base

class Book(Base):
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    year = Column(Integer)
    image_filename = Column(String, nullable=True)
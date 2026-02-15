from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from db.connection import Base

class Loan(Base):
    __tablename__ = "loans"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    timestamp = Column(DateTime, default=datetime.now)
    return_date = Column(DateTime, nullable=True)
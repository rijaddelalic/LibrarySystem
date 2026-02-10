from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.connection import Base, get_session

class TransactionORM(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    book_title = Column(String, nullable=False)
    action = Column(String, nullable=False)  # "borrow" ili "return"
    timestamp = Column(DateTime, default=datetime.now)

def create_transaction(user_id: str, book_title: str, action: str) -> None:
    session = get_session()
    new_transaction = TransactionORM(user_id=user_id, book_title=book_title, action=action)
    session.add(new_transaction)
    session.commit()
    session.close()

def get_transactions():
    session = get_session()
    transactions = session.query(TransactionORM).all()
    session.close()
    return transactions
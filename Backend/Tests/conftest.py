import pytest
from db.connection import get_session
from db.book_dao import BookORM
from db.user_dao import UserORM
from db.transaction_dao import TransactionORM

@pytest.fixture(autouse=True)
def clean_db():
    session = get_session()
    # obriši sve redove iz tabela
    session.query(BookORM).delete()
    session.query(UserORM).delete()
    session.query(TransactionORM).delete()
    session.commit()
    session.close()

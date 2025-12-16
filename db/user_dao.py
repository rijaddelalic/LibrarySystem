from sqlalchemy import Column, Integer, String
from db.connection import Base, get_session

class UserORM(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    membershipId = Column(String, unique=True, nullable=False)


def create_user(name: str, lastname: str, membershipId: str) -> None:
    session = get_session()
    existing = session.query(UserORM).filter_by(membershipId=membershipId).first()
    if existing:
        print(f"  User with membership ID {membershipId} already exists.")
    else:
        new_user = UserORM(name=name, lastname=lastname, membershipId=membershipId)
        session.add(new_user)
        session.commit()
    session.close()

def get_users():
    session = get_session()
    users = session.query(UserORM).all()
    session.close()
    return users

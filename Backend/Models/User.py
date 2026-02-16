from sqlalchemy import Column, Integer, String
from db.connection import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    membershipId = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    profile_image = Column(String, nullable=True)
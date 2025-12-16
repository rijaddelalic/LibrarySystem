from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

engine = create_engine("sqlite:///library.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL za SQLite bazu (možeš promijeniti na PostgreSQL/MySQL ako bude trebalo)
DATABASE_URL = "sqlite:///./library.db"

# Engine za konekciju
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazna klasa za modele
Base = declarative_base()

# Funkcija za dobavljanje sesije (koristi se u Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

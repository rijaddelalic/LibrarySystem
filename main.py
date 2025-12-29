from fastapi import FastAPI
from db.connection import Base, engine
from routers import users, books, loans, stats   # dodaj stats ovdje

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library System API")

# Registracija svih routera
app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(stats.router)   # uključi stats router

@app.get("/")
def root():
    return {"message": "Library System API radi!"}
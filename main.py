from fastapi import FastAPI
from db.connection import Base, engine
from routers import users, books, loans

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library System API")

app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)

@app.get("/")
def root():
    return {"message": "API radi!"}

from fastapi import FastAPI
from db.connection import Base, engine
from Routers import users, books, loans, stats   # dodaj stats ovdje
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library System API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Registracija svih routera
app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(stats.router)   # uključi stats router

@app.get("/")
def root():
    return {"message": "Library System API radi!"}
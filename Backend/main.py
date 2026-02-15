import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db.connection import Base, engine
from Routers import users, books, loans, stats

# 1. Kreiraj tabele
Base.metadata.create_all(bind=engine)

# 2. Inicijalizuj aplikaciju (OVO MORA BITI PRVO)
app = FastAPI(title="Library System API")

# 3. Podesi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Napravi folder za slike ako ne postoji
if not os.path.exists("static/images"):
    os.makedirs("static/images", exist_ok=True)

# 5. Mount-aj static folder (SAD OVO RADI JER JE 'app' DEFINISAN IZNAD)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 6. Registruj routere
app.include_router(users.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(stats.router)

@app.get("/")
def root():
    return {"message": "Library System API radi!"}
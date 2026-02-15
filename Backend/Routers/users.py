from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.User import User
from db.connection import get_db
from Schemas.schemas import UserOut, UserCreate
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

# --- REGISTRACIJA / KREIRANJE KORISNIKA ---
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Provjera da li je Membership ID (Broj karte) već zauzet
    existing_member = db.query(User).filter(User.membershipId == user.membershipId).first()
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail=f"Broj članske karte '{user.membershipId}' je već registrovan!"
        )

    # 2. Provjera da li je Email već zauzet
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Korisnik sa ovom email adresom već postoji!"
        )

    # 3. Kreiranje novog korisnika
    try:
        new_user = User(
            name=user.name,
            lastname=user.lastname,
            membershipId=user.membershipId,
            email=user.email,
            password=user.password # U pravoj app bi ovdje išao hash lozinke
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Greška pri upisu u bazu.")

# --- LISTANJE SVIH KORISNIKA (Za Admin Panel) ---
@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# --- BRISANJE KORISNIKA ---
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen.")

    # Opcionalno: Ovdje bi mogao provjeriti da li korisnik ima zadužene knjige prije brisanja

    db.delete(user)
    db.commit()
    return {"message": "Korisnik uspješno obrisan."}

# --- DETALJI JEDNOG KORISNIKA ---
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen.")
    return user

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Tražimo korisnika po emailu i lozinki
    user = db.query(User).filter(User.email == request.email, User.password == request.password).first()

    if not user:
        raise HTTPException(status_code=401, detail="Pogrešan email ili lozinka")

    return {
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "email": user.email,
        "membershipId": user.membershipId
    }
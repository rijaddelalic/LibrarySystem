import random
import shutil
import os
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from Models.User import User
from db.connection import get_db
from Schemas.schemas import UserOut

router = APIRouter(prefix="/users", tags=["users"])

# --- POMOĆNE FUNKCIJE ZA SIGURNOST (BCRYPT) ---
def hash_pw(pw: str):
    return bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_pw(pw: str, hashed: str):
    return bcrypt.checkpw(pw.encode('utf-8'), hashed.encode('utf-8'))

# --- 1. REGISTRACIJA ---
@router.post("/", response_model=UserOut)
def register(
        name: str = Form(...),
        lastname: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        image: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    # Provjera emaila
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email je već zauzet")

    # Auto-ID Generator (IB-00XXXX)
    while True:
        uid = f"IB-00{random.randint(1000, 9999)}"
        if not db.query(User).filter(User.membershipId == uid).first():
            break

    # Rukovanje slikom
    img_path = None
    if image:
        os.makedirs("static/images", exist_ok=True)
        img_path = f"static/images/u_{uid}_{image.filename}"
        with open(img_path, "wb") as buf:
            shutil.copyfileobj(image.file, buf)

    new_user = User(
        name=name,
        lastname=lastname,
        email=email,
        password=hash_pw(password),
        membershipId=uid,
        profile_image=img_path
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- 2. LOGIN ---
@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_pw(password, user.password):
        raise HTTPException(status_code=401, detail="Pogrešni podaci za prijavu")
    return user

# --- 3. PROMJENA LOZINKE (SETTINGS) ---
@router.put("/{user_id}/change-password")
def change_password(user_id: int, old_pw: str = Form(...), new_pw: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik nije pronađen")

    if not verify_pw(old_pw, user.password):
        raise HTTPException(status_code=400, detail="Trenutna lozinka je netačna")

    user.password = hash_pw(new_pw)
    db.commit()
    return {"msg": "Lozinka uspješno promijenjena"}

# --- 4. ZABORAVLJENA LOZINKA (RESET) ---
@router.put("/reset-password-external")
def reset_password(email: str = Form(...), mid: str = Form(...), new_pw: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email, User.membershipId == mid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Podaci (email/ID) se ne podudaraju!")

    user.password = hash_pw(new_pw)
    db.commit()
    return {"msg": "Lozinka uspješno resetovana"}

# --- 5. ADMIN RUTE ---
@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"msg": "ok"}
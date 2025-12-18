from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user(name: str, lastname: str, membershipId: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.membershipId == membershipId).first():
        raise HTTPException(status_code=400, detail="Membership ID already exists")
    new_user = User(name=name, lastname=lastname, membershipId=membershipId)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

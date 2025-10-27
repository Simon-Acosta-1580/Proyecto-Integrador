from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import User, UserCreate
from utils import soft_delete, restore

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=User)
def create_user(payload: UserCreate, session: Session = Depends(get_session)):
    user = User.from_orm(payload)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/", response_model=list[User])
def get_users(session: Session = Depends(get_session)):
    statement = select(User).where(User.activo == True)
    users = session.exec(statement).all()
    return users

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user or not user.activo:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=User)
def update_user(user_id: int, payload: UserCreate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user or not user.activo:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = payload.name
    user.email = payload.email
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    soft_delete(user, session)
    return {"detail": "User soft-deleted"}

@router.patch("/{user_id}/restore")
def restore_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    restore(user, session)
    return {"detail": "User restored"}

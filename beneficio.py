# beneficio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Beneficio, BeneficioBase
from utils import soft_delete, restore

router = APIRouter(prefix="/beneficios", tags=["beneficios"])

@router.post("/", response_model=Beneficio)
def create_beneficio(payload: BeneficioBase, session: Session = Depends(get_session)):
    b = Beneficio.from_orm(payload)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b

@router.get("/", response_model=list[Beneficio])
def list_beneficios(session: Session = Depends(get_session)):
    return session.exec(select(Beneficio).where(Beneficio.activo == True)).all()

@router.get("/{bid}", response_model=Beneficio)
def get_beneficio(bid: int, session: Session = Depends(get_session)):
    b = session.get(Beneficio, bid)
    if not b or not b.activo:
        raise HTTPException(status_code=404, detail="Not found")
    return b

@router.delete("/{bid}")
def delete_beneficio(bid: int, session: Session = Depends(get_session)):
    b = session.get(Beneficio, bid)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    soft_delete(b, session)
    return {"detail": "Beneficio soft-deleted"}

@router.patch("/{bid}/restore")
def restore_beneficio(bid: int, session: Session = Depends(get_session)):
    b = session.get(Beneficio, bid)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    restore(b, session)
    return {"detail": "Beneficio restored"}

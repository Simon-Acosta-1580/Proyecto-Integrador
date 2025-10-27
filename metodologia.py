
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Metodologia, MetodologiaBase, User
from utils import soft_delete, restore

router = APIRouter(prefix="/metodologias", tags=["metodologias"])

@router.post("/", response_model=Metodologia)
def create_metodologia(payload: MetodologiaBase, session: Session = Depends(get_session)):
    # payload should contain usuario_id in real use; here we assume setting later or include field
    metod = Metodologia.from_orm(payload)
    session.add(metod)
    session.commit()
    session.refresh(metod)
    return metod

@router.get("/", response_model=list[Metodologia])
def list_metodologias(session: Session = Depends(get_session)):
    return session.exec(select(Metodologia).where(Metodologia.activo == True)).all()

@router.get("/{mid}", response_model=Metodologia)
def get_metodologia(mid: int, session: Session = Depends(get_session)):
    m = session.get(Metodologia, mid)
    if not m or not m.activo:
        raise HTTPException(status_code=404, detail="Not found")
    return m

@router.delete("/{mid}")
def delete_metodologia(mid: int, session: Session = Depends(get_session)):
    m = session.get(Metodologia, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Not found")
    soft_delete(m, session)
    return {"detail": "Metodologia soft-deleted"}

@router.patch("/{mid}/restore")
def restore_metodologia(mid: int, session: Session = Depends(get_session)):
    m = session.get(Metodologia, mid)
    if not m:
        raise HTTPException(status_code=404, detail="Not found")
    restore(m, session)
    return {"detail": "Metodologia restored"}

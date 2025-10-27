# analisis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Analisis, AnalisisBase, Metodologia, Beneficio, AnalisisBeneficioLink
from utils import generar_pdf_reporte_analisis, file_response_pdf, soft_delete, restore

router = APIRouter(prefix="/analisis", tags=["analisis"])

@router.post("/", response_model=Analisis)
def create_analisis(payload: AnalisisBase, session: Session = Depends(get_session)):
    # payload.metodologia_id should be present if linking
    anal = Analisis.from_orm(payload)
    session.add(anal)
    session.commit()
    session.refresh(anal)
    return anal

@router.get("/", response_model=list[Analisis])
def list_analisis(session: Session = Depends(get_session)):
    return session.exec(select(Analisis).where(Analisis.activo == True)).all()

@router.get("/{aid}", response_model=Analisis)
def get_analisis(aid: int, session: Session = Depends(get_session)):
    a = session.get(Analisis, aid)
    if not a or not a.activo:
        raise HTTPException(status_code=404, detail="Not found")
    return a

@router.delete("/{aid}")
def delete_analisis(aid: int, session: Session = Depends(get_session)):
    a = session.get(Analisis, aid)
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    soft_delete(a, session)
    return {"detail": "Analisis soft-deleted"}

@router.patch("/{aid}/restore")
def restore_analisis(aid: int, session: Session = Depends(get_session)):
    a = session.get(Analisis, aid)
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    restore(a, session)
    return {"detail": "Analisis restored"}

# Link/unlink Beneficio to Analisis (N:M helpers)
@router.post("/{aid}/beneficios/{bid}")
def link_beneficio(aid: int, bid: int, session: Session = Depends(get_session)):
    a = session.get(Analisis, aid)
    b = session.get(Beneficio, bid)
    if not a or not b:
        raise HTTPException(status_code=404, detail="Not found")
    # create link
    link = AnalisisBeneficioLink(analisis_id=aid, beneficio_id=bid)
    session.add(link)
    session.commit()
    return {"detail": "linked"}

@router.delete("/{aid}/beneficios/{bid}")
def unlink_beneficio(aid: int, bid: int, session: Session = Depends(get_session)):
    stmt = session.exec(select(AnalisisBeneficioLink).where(
        (AnalisisBeneficioLink.analisis_id == aid) & (AnalisisBeneficioLink.beneficio_id == bid)
    )).one_or_none()
    if not stmt:
        raise HTTPException(status_code=404, detail="link not found")
    session.delete(stmt)
    session.commit()
    return {"detail": "unlinked"}

# PDF report endpoint
@router.get("/report/pdf")
def reporte_pdf(session: Session = Depends(get_session)):
    analisis_objs = session.exec(select(Analisis).where(Analisis.activo == True)).all()
    # build data structure of dicts
    lista = []
    for a in analisis_objs:
        beneficios = []
        for b in a.beneficios:
            # ensure activo
            if getattr(b, "activo", True):
                beneficios.append({"categoria": b.categoria, "ingreso": b.ingreso})
        lista.append({
            "id": a.id,
            "nombre": a.nombre,
            "impacto_total": a.impacto_total,
            "alcance_medios": a.alcance_medios,
            "participacion_redes": a.participacion_redes,
            "beneficios": beneficios
        })
    path = generar_pdf_reporte_analisis(lista)
    return file_response_pdf(path)

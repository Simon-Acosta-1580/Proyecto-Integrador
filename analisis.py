from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlmodel import Session, select
from typing import Optional

from db import get_session
from models import Analisis, Metodologia

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def list_analisis(request: Request, session: Session = Depends(get_session)):
    analisis_list = session.exec(
        select(Analisis).where(Analisis.status == True)
    ).all()

    return request.app.state.templates.TemplateResponse(
        "analisis_list.html",
        {"request": request, "analisis_list": analisis_list}
    )

@router.get("/new", response_class=HTMLResponse)
def crear_analisis_form(request: Request, session: Session = Depends(get_session)):
    metodologias = session.exec(select(Metodologia).where(Metodologia.status == True)).all()

    return request.app.state.templates.TemplateResponse(
        "new?analisis.html",
        {"request": request, "metodologias": metodologias}
    )


@router.post("/new")
async def crear_analisis(
        nombre: str = Form(...),
        alcance_medios: float = Form(0),
        participacion_redes: float = Form(0),
        metodologia_id: int = Form(...),
        status: Optional[str] = Form(None),
        session: Session = Depends(get_session)
):
    status_bool = True if status == 'on' else False

    nuevo_analisis = Analisis(
        nombre=nombre,
        alcance_medios=alcance_medios,
        participacion_redes=participacion_redes,
        metodologia_id=metodologia_id,
        status=status_bool,
    )

    session.add(nuevo_analisis)
    session.commit()
    session.refresh(nuevo_analisis)

    return RedirectResponse(f"/analisis/{nuevo_analisis.id}", status_code=HTTP_303_SEE_OTHER)

@router.get("/{analisis_id}", response_class=HTMLResponse)
async def get_one_analisis(
        request: Request,
        analisis_id: int,
        session: Session = Depends(get_session)
):
    analisis = session.exec(
        select(Analisis).where(Analisis.id == analisis_id)
    ).first()

    if not analisis:
        return HTMLResponse("Análisis no encontrado", status_code=404)

    session.refresh(analisis, ["metodologia"])

    return request.app.state.templates.TemplateResponse(
        "analisis_detail.html",
        {"request": request, "analisis": analisis}
    )

@router.get("/editar/{analisis_id}", response_class=HTMLResponse)
def editar_analisis_form(
        analisis_id: int,
        request: Request,
        session: Session = Depends(get_session)
):
    analisis = session.get(Analisis, analisis_id)
    if not analisis:
        return HTMLResponse("Análisis no encontrado", status_code=404)

    metodologias = session.exec(select(Metodologia).where(Metodologia.status == True)).all()

    return request.app.state.templates.TemplateResponse(
        "analisis_edit.html",
        {"request": request, "analisis": analisis, "metodologias": metodologias}
    )

@router.post("/editar/{analisis_id}")
async def editar_analisis(
        analisis_id: int,
        nombre: str = Form(...),
        alcance_medios: float = Form(...),
        participacion_redes: float = Form(...),
        metodologia_id: int = Form(...),
        status: Optional[str] = Form(None),  # Capturamos 'on' o None
        session: Session = Depends(get_session)
):
    analisis = session.get(Analisis, analisis_id)
    if not analisis:
        return HTMLResponse("Análisis no encontrado", status_code=404)

    status_bool = True if status == 'on' else False

    analisis.nombre = nombre
    analisis.alcance_medios = alcance_medios
    analisis.participacion_redes = participacion_redes
    analisis.metodologia_id = metodologia_id
    analisis.status = status_bool
    session.add(analisis)
    session.commit()
    session.refresh(analisis)

    return RedirectResponse(f"/analisis/{analisis.id}", status_code=HTTP_303_SEE_OTHER)


@router.get("/eliminar/{analisis_id}")
def eliminar_analisis(
        analisis_id: int,
        session: Session = Depends(get_session)
):
    analisis = session.get(Analisis, analisis_id)
    if analisis:
        analisis.status = False
        session.add(analisis)
        session.commit()

    return RedirectResponse("/analisis", status_code=HTTP_303_SEE_OTHER)

@router.get("/eliminados", response_class=HTMLResponse)
def analisis_eliminados(request: Request, session: Session = Depends(get_session)):
    analisis_list = session.exec(
        select(Analisis).where(Analisis.status == False)
    ).all()

    return request.app.state.templates.TemplateResponse(
        "analisis_eliminados.html",
        {"request": request, "analisis_list": analisis_list}
    )

@router.get("/restaurar/{analisis_id}")
def restaurar_analisis(
        analisis_id: int,
        session: Session = Depends(get_session)
):
    analisis = session.get(Analisis, analisis_id)
    if analisis:

        analisis.status = True
        session.add(analisis)
        session.commit()

    return RedirectResponse("/analisis/eliminados", status_code=HTTP_303_SEE_OTHER)
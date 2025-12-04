from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import get_session
from models import Metodologia, User
from typing import Optional

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def listar_metodologias(request: Request, session: Session = Depends(get_session)):

    metodologias = session.exec(
        select(Metodologia)
    ).all()

    return request.app.state.templates.TemplateResponse(
        "list_metodologias.html",
        {"request": request, "metodologias": metodologias}
    )

@router.get("/metodologias/new", response_class=HTMLResponse)
def nueva_metodologia_form(request: Request, session: Session = Depends(get_session)):
    users = session.exec(
        select(User).where(User.status == 'Alive')
    ).all()

    return request.app.state.templates.TemplateResponse(
        "new_metodologia.html",
        {"request": request, "users": users}
    )


@router.post("/metodologias/new")
def crear_metodologia(
        titulo: str = Form(...),
        descripcion: str = Form(None),
        user_id: int = Form(...),

        session: Session = Depends(get_session)
):

    metodologia = Metodologia(
        titulo=titulo,
        descripcion=descripcion,
        user_id=user_id,
        status=True
    )

    session.add(metodologia)
    session.commit()
    session.refresh(metodologia)

    return RedirectResponse("/metodologias", status_code=HTTP_303_SEE_OTHER)


@router.get("/{metodologia_id}", response_class=HTMLResponse)
async def get_one_metodologia(
        request: Request,
        metodologia_id: int,
        session: Session = Depends(get_session)
):
    metodologia = session.exec(
        select(Metodologia).where(Metodologia.id == metodologia_id)
    ).first()

    if not metodologia:
        return RedirectResponse("/metodologias", status_code=HTTP_303_SEE_OTHER)

    session.refresh(metodologia, ["usuario", "analisis"])

    return request.app.state.templates.TemplateResponse(
        "metodologia_detail.html",
        {"request": request, "metodologia": metodologia}
    )

@router.get("/editar/{metodologia_id}", response_class=HTMLResponse)
def editar_metodologia_form(
        metodologia_id: int,
        request: Request,
        session: Session = Depends(get_session)
):
    metodologia = session.get(Metodologia, metodologia_id)
    if not metodologia:
        return HTMLResponse("Metodología no encontrada", status_code=404)

    users = session.exec(select(User)).all()

    return request.app.state.templates.TemplateResponse(
        "metodologia_edit.html",
        {"request": request, "metodologia": metodologia, "users": users}
    )

@router.post("/editar/{metodologia_id}")
async def editar_metodologia(
        metodologia_id: int,
        titulo: str = Form(...),
        descripcion: Optional[str] = Form(None),
        user_id: int = Form(...),
        status: Optional[str] = Form(None),  # Capturamos 'on' o None
        session: Session = Depends(get_session)
):
    metodologia = session.get(Metodologia, metodologia_id)
    if not metodologia:
        return HTMLResponse("Metodología no encontrada", status_code=404)

    status_bool = True if status == 'on' else False

    metodologia.titulo = titulo
    metodologia.descripcion = descripcion
    metodologia.user_id = user_id
    metodologia.status = status_bool

    session.add(metodologia)
    session.commit()
    session.refresh(metodologia)

    return RedirectResponse(f"/metodologia/{metodologia.id}", status_code=HTTP_303_SEE_OTHER)


@router.get("/eliminar/{metodologia_id}")
def eliminar_metodologia(
        metodologia_id: int,
        session: Session = Depends(get_session)
):
    metodologia = session.get(Metodologia, metodologia_id)
    if metodologia:
        metodologia.status = False
        session.add(metodologia)
        session.commit()

    return RedirectResponse("/metodologias", status_code=HTTP_303_SEE_OTHER)


@router.get("/eliminados", response_class=HTMLResponse)
def metodologias_eliminadas(request: Request, session: Session = Depends(get_session)):
    metodologias = session.exec(
        select(Metodologia).where(Metodologia.status == False)
    ).all()

    return request.app.state.templates.TemplateResponse(
        "metodologia_eliminados.html",
        {"request": request, "metodologias": metodologias}
    )


@router.get("/restaurar/{metodologia_id}")
def restaurar_metodologia(
        metodologia_id: int,
        session: Session = Depends(get_session)
):
    metodologia = session.get(Metodologia, metodologia_id)
    if metodologia:
        metodologia.status = True
        session.add(metodologia)
        session.commit()

    return RedirectResponse("/metodologia/eliminados", status_code=HTTP_303_SEE_OTHER)
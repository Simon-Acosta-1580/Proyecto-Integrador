from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import get_session
from models import Metodologia, User

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
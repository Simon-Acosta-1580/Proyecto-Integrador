from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import get_session
from models import User
from Supabase.supabase_upload import upload_to_bucket

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def listado_users_html(request: Request, session: Session = Depends(get_session)):
    users = session.exec(select(User).where(User.status == True)).all()
    return request.app.state.templates.TemplateResponse(
        "user_list.html",
        {"request": request, "users": users}
    )

@router.get("/new", response_class=HTMLResponse)
def formulario_nuevo_user(request: Request):
    return request.app.state.templates.TemplateResponse(
        "new_user.html",
        {"request": request}
    )

@router.post("/new")
async def crear_user(
    name: str = Form(...),
    email: str = Form(...),
    role: bool = Form(...),
    status: str = Form(...),
    img: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    img_url = None

    if img:
        img_url = await upload_to_bucket(img, "users")

    nuevo_user = User(
        name=name,
        email=email,
        role=role,
        status=status,
        img=img_url,
    )

    session.add(nuevo_user)
    session.commit()
    session.refresh(nuevo_user)

    return RedirectResponse("/users", status_code=HTTP_303_SEE_OTHER)


@router.get("/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int, session: Session=Depends(get_session)):
    user_db = await session.get(User, user_id)
    if not user_db:
        return HTMLResponse("User no encontrado", status_code=404)
    await session.refresh(user_db, ["metodologias"])
    return request.app.state.templates.TemplateResponse("user_detail.html", {"request": request, "user": user_db})

@router.get("/editar/{user_id}", response_class=HTMLResponse)
def editar_user_form(user_id: int, request: Request, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        return HTMLResponse("Usuario no encontrado", status_code=404)

    return request.app.state.templates.TemplateResponse(
        "user_edit.html",
        {"request": request, "user": user}
    )

@router.post("/editar/{user_id}")
async def editar_user(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    role: bool = Form(...),
    status: str = Form(True),
    img: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        return HTMLResponse("User no encontrado", status_code=404)

    user.name = name
    user.email = email
    user.role = role
    user.status = status


    if img:
        user.img = await upload_to_bucket(img, "users")

    session.add(user)
    session.commit()

    return RedirectResponse("/users", status_code=HTTP_303_SEE_OTHER)

@router.get("/eliminar/{user_id}")
def eliminar_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user:
        user.status = False
        session.add(user)
        session.commit()

    return RedirectResponse("/users", status_code=HTTP_303_SEE_OTHER)



@router.get("/eliminados", response_class=HTMLResponse)
def eliminados(request: Request, session: Session = Depends(get_session)):
    users = session.exec(select(User).where(User.status == False)).all()

    return request.app.state.templates.TemplateResponse(
        "user_eliminados.html",
        {"request": request, "users": users}
    )



@router.get("/restaurar/{user_id}")
def restaurar_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user:
        user.status = True
        session.add(user)
        session.commit()

    return RedirectResponse("/users/eliminados", status_code=HTTP_303_SEE_OTHER)
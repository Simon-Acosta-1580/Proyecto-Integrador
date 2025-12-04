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
    users = session.exec(select(User).where(User.active == True)).all()
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
        active=True
    )

    session.add(nuevo_user)
    session.commit()
    session.refresh(nuevo_user)

    return RedirectResponse("/users", status_code=HTTP_303_SEE_OTHER)


@router.get("/{user_id}", response_class=HTMLResponse)
async def get_one_user(request: Request, user_id: int, session: Session=Depends(get_session)):
    user_db = await session.get(User, user_id)
    if not user_db:
        return HTMLResponse("Cliente no encontrado", status_code=404)
    await session.refresh(user_db, ["metodologias"])
    return request.app.state.templates.TemplateResponse("user_detail.html", {"request": request, "user": user_db})

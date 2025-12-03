from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import get_session
from models import User
from Supabase.supabase_upload import upload_to_bucket

router = APIRouter()


@router.get("/new", response_class=HTMLResponse)
def formulario_nuevo_user(request: Request):
    return request.app.state.templates.TemplateResponse(
        "new_user.html",
        {"request": request}
    )



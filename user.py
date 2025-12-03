from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import get_session
from models import User
from supabase.supabase_upload import upload_to_bucket

router = APIRouter()

templates = Jinja2Templates(directory="Templates")

@router.get("/new", response_class=HTMLResponse)
async def show_create(request: Request):
    return templates.TemplateResponse("new_user.html", {"request": request})



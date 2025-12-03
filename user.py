from fastapi.responses import HTMLResponse, RedirectResponse
from db import SessionDep
from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from models import User, UserCreate
from sqlmodel import select
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter()

templates = Jinja2Templates(directory="Templates")

@router.get("/new", response_class=HTMLResponse)
async def show_create(request: Request):
    return templates.TemplateResponse("new_user.html", {"request": request})



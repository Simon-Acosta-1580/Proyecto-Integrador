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

@router.post("/", response_model=User, status_code=201)
async def create_user(request: Request,
                      session: SessionDep,
                      name: str = Form(...),
                      year: int = Form(...),
                      status: bool = Form(True),
                      img: Optional[UploadFile] = File(None)
                      ):
    try:
        new_user = UserCreate(name=name, year=year, status=status, img=img_url)

        user = User.model_validate(new_user)
        session.add(user)
        await session.commit()
        await session.refresh(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return RedirectResponse(url=f"/users/{user.id}", status_code=302)


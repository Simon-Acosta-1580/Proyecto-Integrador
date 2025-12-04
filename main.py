from fastapi import FastAPI, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from starlette.status import HTTP_303_SEE_OTHER
from db import create_tables, get_session
from user import router as user_router
from metodologia import router as metodologia_router
from analisis import router as analisis_router
from beneficio import router as beneficio_router
from Supabase.supabase_upload import upload_to_bucket
from supabase import create_client


app = FastAPI(title="Proyecto impacto Mundial FIFA API")

templates = Jinja2Templates(directory="Templates")


app.state.templates = templates

@app.on_event("startup")
def on_startup():
    create_tables()
    print("Base de datos inicializada y servidor listo.")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(metodologia_router,prefix="/metodologias", tags=["metodologias"])
app.include_router(analisis_router, prefix="/analisis", tags=["analisis"])
app.include_router(beneficio_router, prefix="/beneficios", tags=["beneficios"])

@app.get("/", response_class=HTMLResponse, tags=["Vistas HTML"])
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "texto": "Bienvenido a la API del Mundial FIFA",
        }
    )
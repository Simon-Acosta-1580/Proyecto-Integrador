from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db import create_tables
import user
import metodologia
import analisis
import beneficio
from fastapi.staticfiles import StaticFiles
import images

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables(app)
    yield

app = FastAPI(lifespan=create_tables, title="Proyecto Integrador")

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/img", StaticFiles(directory="upload"), name="img")
app.include_router(user.router, prefix="/users", tags=["Usuarios"])
app.include_router(metodologia.router, prefix="/metodologia", tags=["Metodología"])
app.include_router(analisis.router, prefix="/analisis", tags=["Análisis"])
app.include_router(beneficio.router, prefix="/beneficios", tags=["Beneficios"])

templates = Jinja2Templates(directory="templates")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    result = await images.upload_file(file)
    return result


@app.get("/", response_class=HTMLResponse, status_code=200)
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/hello/{name}", response_class=HTMLResponse)
async def say_hello(request: Request, name: str):
    return templates.TemplateResponse(
        request=request,
        name="hello.html",
        context={"texto": name.upper()}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "status_code": exc.status_code, "detail": exc.detail},
        status_code=exc.status_code,
    )

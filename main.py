# main.py
from fastapi import FastAPI
from db import create_db_and_tables
from user import router as user_router
from metodologia import router as metodologia_router
from analisis import router as analisis_router
from beneficio import router as beneficio_router

app = FastAPI(title="Proyecto - Mundial Impacto")

# Crear tablas al arrancar
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_router)
app.include_router(metodologia_router)
app.include_router(beneficio_router)
app.include_router(analisis_router)

@app.get("/")
def root():
    return {"message": "API is running"}

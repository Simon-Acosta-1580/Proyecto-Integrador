from fastapi import FastAPI
from db import create_tables
from user import router as user_router
from metodologia import router as metodologia_router
from analisis import router as analisis_router
from beneficio import router as beneficio_router



app = FastAPI(lifespan=create_tables, title="Proyecto Integrador")
app.include_router(user_router)
app.include_router(user_router, prefix="/users", tags=["Usuarios"])
app.include_router(metodologia_router, prefix="/metodologia", tags=["Metodología"])
app.include_router(analisis_router, prefix="/analisis", tags=["Análisis"])
app.include_router(beneficio_router, prefix="/beneficios", tags=["Beneficios"])


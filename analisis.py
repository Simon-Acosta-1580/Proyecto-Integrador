# analisis.py
from fastapi import APIRouter,HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Analisis, AnalisisBase, Beneficio, AnalisisBeneficioLink

router = APIRouter(prefix="/analisis", tags=["analisis"])


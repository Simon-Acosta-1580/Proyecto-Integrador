from fastapi import APIRouter,HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Analisis, AnalisisBase, Beneficio

router = APIRouter(prefix="/analisis", tags=["analisis"])


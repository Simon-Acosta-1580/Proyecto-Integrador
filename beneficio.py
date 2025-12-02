from fastapi import APIRouter,HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Beneficio, BeneficioBase

router = APIRouter(prefix="/beneficios", tags=["beneficios"])


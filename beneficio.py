from fastapi import APIRouter,HTTPException, status
from sqlmodel import select
from db import create_tables
from models import Beneficio, BeneficioBase

router = APIRouter()


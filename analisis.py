# analisis.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Analisis, AnalisisBase, Beneficio, AnalisisBeneficioLink

router = APIRouter(prefix="/analisis", tags=["analisis"])


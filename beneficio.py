# beneficio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Beneficio, BeneficioBase

router = APIRouter(prefix="/beneficios", tags=["beneficios"])


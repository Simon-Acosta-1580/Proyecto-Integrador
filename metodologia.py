
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import create_tables
from sqlmodel import Session
from models import Metodologia, MetodologiaBase

router = APIRouter(prefix="/metodologias", tags=["metodologias"])


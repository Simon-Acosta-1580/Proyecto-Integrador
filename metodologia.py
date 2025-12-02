
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import Metodologia, MetodologiaBase
from utils import soft_delete, restore

router = APIRouter(prefix="/metodologias", tags=["metodologias"])


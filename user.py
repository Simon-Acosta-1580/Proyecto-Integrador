from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from db import get_session
from sqlmodel import Session
from models import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])



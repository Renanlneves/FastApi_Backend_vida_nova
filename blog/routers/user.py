from fastapi import APIRouter
from config import database
from domain.account import schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from domain.account.hashing import Hash
from repository import user

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

get_db = database.get_db


@router.post("/", response_model=schemas.Show_user)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)
    
 

@router.get("/{id}", response_model=schemas.Show_user)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.show(id, db)

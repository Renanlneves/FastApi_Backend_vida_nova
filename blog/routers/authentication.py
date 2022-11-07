import re
from fastapi import APIRouter, Depends, HTTPException, status
from domain.account import schemas, models
from config import database
from sqlalchemy.orm import Session
from domain.account.hashing import Hash


router = APIRouter(
    tags=["authentication"]
)

@router.post("/login")
def login(request:schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Credenciais invalidas")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Senha incorreta")

    #gerar um token jwt e retornar    

    return user 

    
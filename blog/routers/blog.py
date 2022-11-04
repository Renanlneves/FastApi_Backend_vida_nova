
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from domain.account import schemas, models
from config import database
from sqlalchemy.orm import Session
from repository import blog

get_db = database.get_db
router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)



@router.get("/", response_model=List[schemas.Showblog]) #pegando todos os dados/ USANDO O modelo de resposta do schema para sair em formato lista
def all(db: Session = Depends(get_db)):
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED) #status_code define o tipo de status que queremos ao executar
def create(request: schemas.Blog, db: Session = Depends(get_db)):
   return blog.create(request, db)

@router.get("/{id}", status_code=200, response_model=schemas.Showblog) #pegando um determinado dados pela id
def show(id: int, db: Session = Depends(get_db)):
    return blog.show(id, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    return blog.destroy(id, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(id, request, db)




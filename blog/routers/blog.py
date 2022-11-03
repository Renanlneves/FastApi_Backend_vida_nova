
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from domain.account import schemas, models
from config import database
from sqlalchemy.orm import Session

get_db = database.get_db
router = APIRouter()

@router.get("/blog", response_model=list[schemas.Showblog], tags=["blogs"]) #pegando todos os dados/ USANDO O modelo de resposta do schema para sair em formato lista
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"]) #status_code define o tipo de status que queremos ao executar
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/blog/{id}", status_code=200, response_model=schemas.Showblog, tags=["blogs"]) #pegando um determinado dados pela id
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first() # filter funciona como um "where" do sql / first significa que queremos apenas o primeiro
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"O blog de número {id}, não está disponivel.") #erro e mensagem em uma linha
       
    return blog


@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")

    blog.delete(synchronize_session=False)#delete pego na documentação do alchemy
    db.commit() #sempre que fazer uma alteração no banco de dados vc tem que commitar ela
    return "done"


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")


    blog.update(request, tags=["blogs"])
    db.commit()   #SEMPRE PRECISAMOS COMMITAR PARA FAZER UMA ALTERAÇÃO NO CODIGO
    return "updated"




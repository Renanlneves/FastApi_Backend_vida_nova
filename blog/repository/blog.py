from sqlalchemy.orm import Session
from domain.account import models
from domain.account import schemas
from fastapi import HTTPException, status

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db:Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def destroy(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")

    blog.delete(synchronize_session=False)#delete pego na documentação do alchemy
    db.commit() #sempre que fazer uma alteração no banco de dados vc tem que commitar ela
    return "done"

def update(id:int, request:schemas.Blog, db:Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")


    blog.update(request)
    db.commit()   #SEMPRE PRECISAMOS COMMITAR PARA FAZER UMA ALTERAÇÃO NO CODIGO
    return "updated"

def show(id:int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first() # filter funciona como um "where" do sql / first significa que queremos apenas o primeiro
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"O blog de número {id}, não está disponivel.") #erro e mensagem em uma linha
       
    return blog
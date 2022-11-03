from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import uvicorn
from config.database import SessionLocal
from domain.account import schemas
from domain.account import models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session
from domain.account.hashing import Hash

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"]) #status_code define o tipo de status que queremos ao executar
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=list[schemas.Showblog], tags=["blogs"]) #pegando todos os dados/ USANDO O modelo de resposta do schema para sair em formato lista
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=200, response_model=schemas.Showblog, tags=["blogs"]) #pegando um determinado dados pela id
def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first() # filter funciona como um "where" do sql / first significa que queremos apenas o primeiro
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"O blog de número {id}, não está disponivel.") #erro e mensagem em uma linha
        # response.status_code = status.HTTP_404_NOT_FOUND # usando o response para colocar uma condição que dira um novo status se ativada
        #return {"detalhe" : f"O blog de número {id}, não está disponivel." } 
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")

    blog.delete(synchronize_session=False)#delete pego na documentação do alchemy
    db.commit() #sempre que fazer uma alteração no banco de dados vc tem que commitar ela
    return "done"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog com a id {id}, não encontrado")


    blog.update(request, tags=["blogs"])
    db.commit()   #SEMPRE PRECISAMOS COMMITAR PARA FAZER UMA ALTERAÇÃO NO CODIGO
    return "updated"




@app.post("/user", response_model=schemas.Show_user, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model=schemas.Show_user, tags=["users"])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Usuario com a id {id}, não encontrado")
    
    return user







if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
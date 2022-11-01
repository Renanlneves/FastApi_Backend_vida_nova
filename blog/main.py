from turtle import title
from fastapi import FastAPI, Depends
import uvicorn
from config.database import SessionLocal
from domain.account import schemas
from domain.account import models
from config.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
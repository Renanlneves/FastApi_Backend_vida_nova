from fastapi import FastAPI
import uvicorn
from domain.account import schemas
from domain.account import models
from config.database import engine

app = FastAPI()


models.Base.metadata.create_all(bind=engine)


@app.post("/blog")
def create(request: schemas.Blog):
    return {request}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
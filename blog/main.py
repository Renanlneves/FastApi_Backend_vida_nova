from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
import uvicorn
from config.database import SessionLocal
from domain.account import schemas
from domain.account import models
from config.database import engine, get_db
from sqlalchemy.orm import Session
from domain.account.hashing import Hash
from routers import blog

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)

















if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
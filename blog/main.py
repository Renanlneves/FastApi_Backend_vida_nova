from fastapi import FastAPI
import uvicorn
from domain.account import models
from config.database import engine
from routers import blog, user

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(blog.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
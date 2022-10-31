from fastapi import FastAPI
import uvicorn
import schemas

app = FastAPI()



@app.post("/blog")
def create(request: schemas.Blog):
    return {request}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8038,reload=True)
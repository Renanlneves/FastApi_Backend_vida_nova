from pydantic import BaseModel
from typing import List

class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):
    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

class Show_user(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class Showblog(BaseModel):
    title: str
    body: str
    creator: Show_user

    class Config(): 
        orm_mode = True

class Login(BaseModel):
    username: str
    password: str
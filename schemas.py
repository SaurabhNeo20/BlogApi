
   
from typing import List, Optional
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    body: str
    user_id:int
    
class Blog(BlogBase):
    class Config():
        orm_mode = True

class Comments(BaseModel):
    text:str
    user_id:int
    post_id:int

class User(BaseModel):
    name:str
    email:str
    password:str


class ShowUser(BaseModel):
    name:str
    email:str
    blogs : List[Blog] =[]
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    body:str
    user: ShowUser

    class Config():
        orm_mode = True



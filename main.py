from crypt import crypt
import email
import imp
from unicodedata import name
from fastapi import Depends, FastAPI,Response
import models as models
from sqlalchemy.orm import Session
import schemas as schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from hashing import Hash
from fastapi import HTTPException, status
from passlib.context import CryptContext
SQLALCHAMY_DATABASE_URL = 'sqlite:///./blog.db'

engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

app= FastAPI()
models.Base.metadata.create_all(engine)

# @app.get('/blog')
# def index():
#     return "api for hjgj blog"



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/user',tags=['users'])
def create_newuser(request: schemas.User,db:Session=Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get('/user',tags=['users'])
def get_by_id(id: int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

@app.get('/name',tags=['users'])
def get_by_name(name: str, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.name== name).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with this name {name} is not available")
    return user


@app.post('/post',tags=['Post'])
def create(request:schemas.Blog,db:Session=Depends(get_db)):
    new_post=models.Blog(title=request.title,body=request.body,user_id=request.user_id)
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id is not available")
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return request



@app.get('/post',tags=['Post'])
def all(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/post/{id}',tags=['Post'])
def get_by_ids(id,response:Response,db:Session=Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not post:
        response.status_code=status.HTTP_404_NOT_FOUND

    return post




@app.get('/post/title',tags=['Post'])
def get_by_tilte(title: str, db:Session=Depends(get_db)):
    title = db.query(models.Blog).filter(models.Blog.title== title).all()
    if not title:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with this name {title} is not available")
    return title


@app.post('/comments',tags=['comments'])
def create_post(request:schemas.Comments,db:Session=Depends(get_db)):
    test=models.Comment(text=request.text,post_id=request.post_id,user_id=request.user_id)
    new_comment = db.query(models.Blog).filter(models.Blog.id== request.post_id).first()
    if not new_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with this name {new_comment} is not available")
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment 
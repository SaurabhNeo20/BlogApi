from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from sqlalchemy import create_engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    password = Column(String)
    # username=Column(String,unique=True)

    blogs = relationship('Blog', back_populates="user")

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=True)
    body = Column(String)
    
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="blogs")



class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key = True)
    text = Column(String,nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('blogs.id'))
 





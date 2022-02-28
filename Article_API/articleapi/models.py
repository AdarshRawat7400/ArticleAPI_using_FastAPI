from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from articleapi.database import Base
from sqlalchemy.orm import relationship


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    body = Column(String)
    published = Column(Boolean, default=True)  
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="articles")    
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    articles = relationship("Article", back_populates="author")


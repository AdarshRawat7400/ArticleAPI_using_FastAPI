from pydantic import BaseModel
from typing import Optional,List


class ArticleIn(BaseModel):
    title : str
    description : str = None
    body : str
    published : Optional[bool] = True

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name : str
    username : str

    class Config:
        orm_mode = True

class UserIn(UserBase):
    email : str
    password : str


    
class UserOut(BaseModel):
    name : str
    username : str
    email : str
    articles : List[ArticleIn] = []


    class Config:
        orm_mode = True

    


class ArticleOut(BaseModel):
    title : str
    description : str 
    body : str
    published : bool
    id : int
    author : UserBase


    class Config:
        orm_mode = True
    
class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
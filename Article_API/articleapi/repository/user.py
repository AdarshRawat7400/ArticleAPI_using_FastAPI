
from sqlalchemy.orm import Session
from fastapi import Depends, status, Response, HTTPException,BackgroundTasks
from articleapi import models, schemas
from articleapi.hashing import Hash
from fastapi_mail import FastMail,ConnectionConfig,MessageSchema
from decouple import config

conf = ConnectionConfig(
MAIL_USERNAME = config('MAIL_USERNAME'),
MAIL_PASSWORD = config('MAIL_PASSWORD'),
MAIL_FROM = config('MAIL_FROM'),
MAIL_PORT = config('MAIL_PORT',cast=int),
MAIL_SERVER = config('MAIL_SERVER'),
MAIL_FROM_NAME = config('MAIL_FROM_NAME'),
MAIL_TLS = True,
MAIL_SSL = False,
USE_CREDENTIALS = True,
VALIDATE_CERTS = True
)

def send_email_background(subject: str, email_to: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body = [ ]
    )
    
    fm = FastMail(conf)
    print("Sending Email")
    background_tasks = BackgroundTasks()
    print('type of background task',background_tasks)
    background_tasks.add_task(
       fm.send_message, message)




def create_user(request : schemas.UserIn,db : Session):
    if db.query(models.User).filter(models.User.username == request.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with username `{request.username}`  already exists")
    if db.query(models.User).filter(models.User.email == request.email).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"User with email `{request.email}`  already exists")
        
    hashed_password = Hash.encrpyt(request.password)
    new_user = models.User(name=request.name, username=request.username,
                            email=request.email, password=hashed_password)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(request.email)
    send_email_background(
                          subject='Welcome to the Article API',
                          email_to=request.email)
    print("STARTED BG TASK")
    return new_user

def get_user(username : str,db : Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username {username} not found")

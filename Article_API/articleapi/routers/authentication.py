from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from articleapi import database,models
from sqlalchemy.orm import Session
from datetime import timedelta
from articleapi.hashing import Hash
from articleapi.token import create_access_token
from decouple import config

router = APIRouter(
    tags=['Authentication']
)



@router.post("/login")
def login(request : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")
    if not Hash.verify(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password!")
    access_token_expires = timedelta(minutes=config('ACCESS_TOKEN_EXPIRE_MINUTES',cast=int))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
   
    return {"access_token": access_token, "token_type": "bearer"}


from fastapi import FastAPI,Depends,status,APIRouter
from articleapi import  schemas,database
from sqlalchemy.orm import Session
from articleapi.repository.user import create_user,get_user


router = APIRouter(
    prefix="/user",
    tags=['Users']
)


get_db = database.get_db

@router.post('',response_model=schemas.UserOut,
                response_model_exclude_none=True,
                status_code=status.HTTP_201_CREATED
                )
def create_user_path(request : schemas.UserIn,db : Session = Depends(get_db)):
    return create_user(request,db)
    


@router.get('/{username}',response_model=schemas.UserOut)
def get_user_path(username : str,db : Session = Depends(get_db)):
    return get_user(username,db)
    


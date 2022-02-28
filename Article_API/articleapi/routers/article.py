from fastapi import APIRouter,Depends,Query,status,Response,HTTPException,Request
from articleapi import models, schemas,database
from typing import Optional, List
from sqlalchemy.orm import Session
from articleapi import oauth2
from articleapi.repository.article import (get_all_articles,create_article,get_article
                                    ,update_article,delete_article)


get_db = database.get_db
router  = APIRouter(
    prefix="/article",
    tags=['Articles']
)




@router.get('',response_model=List[schemas.ArticleOut])
def articles_path(db : Session = Depends(get_db),current_user : schemas.UserIn = Depends(oauth2.get_current_user),ispublished: Optional[bool] = Query(None),username: Optional[str] = Query(None)):
    print("Print Current User",current_user)
    return get_all_articles(ispublished,username,db)    

@router.post('',status_code=status.HTTP_201_CREATED,response_model=schemas.ArticleOut)
def create_article_path(request : schemas.ArticleIn,db : Session = Depends(get_db),current_user : schemas.UserIn = Depends(oauth2.get_current_user)):
    return create_article(request,db,current_user.email)


@router.get('/{article_id}',status_code=status.HTTP_200_OK,response_model=schemas.ArticleOut)
def article_path(article_id : int,response : Response, db : Session = Depends(get_db),current_user : schemas.UserIn = Depends(oauth2.get_current_user)):
    return get_article(article_id,response,db)
    


@router.put('/{article_id}',
        status_code=status.HTTP_202_ACCEPTED,
        response_model=schemas.ArticleOut,
        )
def update_article_path(request : schemas.ArticleIn,
                  article_id : int,
                  db : Session = Depends(get_db),
                  current_user : schemas.UserIn = Depends(oauth2.get_current_user)
                  ):
    return update_article(request,article_id,db,current_user.email)


   

@router.delete('/{article_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_article_path(article_id : int,db : Session = Depends(get_db),
current_user : schemas.UserIn = Depends(oauth2.get_current_user)):
    return delete_article(article_id,db,current_user.email)
   


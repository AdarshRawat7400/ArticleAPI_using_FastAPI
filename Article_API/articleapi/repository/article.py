from sqlalchemy.orm import Session
from fastapi import Depends, status, Response, HTTPException, Query, APIRouter
from articleapi import models, schemas, database



def get_all_articles(ispublished : Query,username : Query,db : Session):
    if username is None and ispublished is None:
        return db.query(models.Article).all()

    if username is None and ispublished is not None:
        return db.query(models.Article).filter(models.Article.published == ispublished).all()
    if username is not None and ispublished is None:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username `{username}` not found")
        return db.query(models.Article).filter(models.Article.user_id == user.id).all()

    if username is not None and ispublished is not None:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username `{username}` not found")
        return db.query(models.Article).filter(models.Article.user_id == user.id).filter(models.Article.published == ispublished).all()

    if username is None and ispublished is not None:
        if ispublished == "true":
            return db.query(models.Article).filter(models.Article.published == True).all()
        if ispublished == "false":
            return db.query(models.Article).filter(models.Article.published == False).all()

def create_article(request: schemas.ArticleIn, db: Session, current_user_email):
    if db.query(models.Article).filter(models.Article.title == request.title).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Article with title `{request.title}`  already exists")

    user = db.query(models.User).filter(models.User.email == current_user_email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")
    
    new_article = models.Article(title=request.title, description=request.description, 
                            body=request.body, published=request.published,user_id = user.id )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_article(article_id : int,response : Response,db : Session):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article:
        return article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {article_id} not found")


def update_article(request : schemas.ArticleIn,article_id : int,db : Session,current_user_email):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article:
        if article.title != request.title  and db.query(models.Article).filter(models.Article.title == request.title).first() is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Article with title `{request.title}`  already exists")
        user = db.query(models.User).filter(models.User.email == current_user_email).first()
        if user:
            if user.id != article.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized Operation `This Article Does Not Belong to You!`")
        article.title = request.title
        article.description = request.description
        article.body = request.body
        article.published = request.published
        db.commit()
        return article
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {article_id} not found")


def delete_article(article_id : int,db : Session,current_user_email):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if article:
        user = db.query(models.User).filter(models.User.email == current_user_email).first()
        if user:
            if user.id != article.user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized Operation `This Article Does Not Belong to You!`")
        db.delete(article)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id {article_id} not found")

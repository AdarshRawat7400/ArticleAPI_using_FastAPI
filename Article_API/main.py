from fastapi import FastAPI
from articleapi.routers import article,user,authentication
from articleapi.api_info import api_details,tags_metadata
from articleapi import models
from articleapi.database import engine
app = FastAPI(
    title=api_details['title'],
    description=api_details['description'],
    version=api_details['version'],
    openapi_tags=tags_metadata
)

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(article.router)





        










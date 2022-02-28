from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL =  "postgresql://zouqtyjlpvpemp:4232d62305cbd08974e917c5377f8e89329af5aade28a6f0e9470381a3320a0f@ec2-52-72-125-94.compute-1.amazonaws.com:5432/d10j57p3ql1nkl"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={}
)

SessionLocal = sessionmaker(autocommit=False,
                             autoflush=False,
                             bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal(bind=engine)
    try:
        yield db
    finally:
        db.close()

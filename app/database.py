from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql
import os

# DEFINE THE DATABASE CREDENTIALS
user = 'sa'
password = 'PXY8ZqgbGHL65Z'
host = os.getenv("DB_HOST")
port = 1433
database = 'LADUPLA'

engine = create_engine(
    url="mssql+pymssql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    ))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
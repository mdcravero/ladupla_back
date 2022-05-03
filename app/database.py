from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymssql

# engine = create_engine(
#     r"mssql+pymssql://{0}:{1}@10.133.0.3:1433/LADUPLA?charset=utf8".format('sqlserver', 'Ladupla2022'))

# DEFINE THE DATABASE CREDENTIALS
user = 'sqlserver'
password = 'Ladupla2022'
host = '34.71.215.9'
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

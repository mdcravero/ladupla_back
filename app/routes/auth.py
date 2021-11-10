from fastapi import APIRouter, status, HTTPException
import models
import schemas
from db.conexion import *
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.params import Depends

auth = APIRouter(tags=['Authentication'])


@auth.post('/login', response_model=schemas.Login)
async def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.EMAIL == request.EMAIL).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.PASSWORD, request.PASSWORD):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    return user

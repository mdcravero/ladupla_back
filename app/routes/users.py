from typing import List
from fastapi import APIRouter, status, HTTPException
import models
import schemas
from db.conexion import *
from sqlalchemy.orm import Session
from hashing import Hash
from fastapi.params import Depends


user = APIRouter(tags=['Users'])


@user.get('/users/', response_model=List[schemas.User])
def show_users(db: Session = Depends(get_db)):
    usuarios = db.query(models.User).all()
    return usuarios


@user.post('/users/', response_model=schemas.User)
def create_users(entrada: schemas.User, db: Session = Depends(get_db)):
    usuario = models.User(USUARIO=entrada.USUARIO,
                          EMAIL=entrada.EMAIL, PASSWORD=Hash.bcrypt(entrada.PASSWORD))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


# UTILS

# @app.put('/usuarios/{usuario_id}', response_model=schemas.User)
# def update_users(usuario_id: int, entrada: schemas.UserUpdate, db: Session = Depends(get_db)):
#     usuario = db.query(models.User).filter_by(id=usuario_id).first()
#     usuario.nombre = entrada.nombre
#     db.commit()
#     db.refresh(usuario)
#     return usuario


# @app.delete('/usuarios/{usuario_id}', response_model=schemas.Respuesta)
# def delete_users(usuario_id: int, db: Session = Depends(get_db)):
#     usuario = db.query(models.User).filter_by(id=usuario_id).first()
#     db.delete(usuario)
#     db.commit()
#     respuesta = schemas.Respuesta(mensaje="Eliminado exitosamente")
#     return respuesta

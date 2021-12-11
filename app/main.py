from typing import List
from fastapi import status, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from . import models
from . import schemas
from .database import get_db, engine
from sqlalchemy.orm import Session
from fastapi.params import Depends
from . import hashing
from datetime import date, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='test FastAPI',
              description='Backend App La Dupla',
              version='1.0')

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=['Documentation'])
def main():
    return RedirectResponse(url="/docs/")


@app.post('/login', response_model=schemas.Login)
async def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.EMAIL == request.EMAIL).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not hashing.Hash.verify(user.PASSWORD, request.PASSWORD):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    return user


@app.get('/bookings/made', tags=['Bookings'], response_model=List[schemas.MadeBooking])
def show_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings


@app.get('/bookings/available', tags=['Bookings'], response_model=List[schemas.ShowBooking])
def show_bookings(db: Session = Depends(get_db)):
    # Configs
    days = 5
    init_hour = 18
    end_hour = 24
    products = db.query(models.Products).filter(
        models.Products.TIPO == 'CAN').all()

    # Days
    today = date.today()
    end = today + timedelta(days=days)

    # All
    booking = []
    for i in range(days):
        for h in range(init_hour, end_hour):
            for p in products:
                booking.append({
                    'COD_PRODUCTO': p.COD_PRODUCTO,
                    'NOMBRE_PRODUCTO': p.DESCRIPCION,
                    'PRECIO_UNIDAD': p.PRECIO_UNIDAD,
                    'FECHA': today + timedelta(days=i),
                    'HORA_INGRESO': str(h) + ":00",
                    "ESTADO": "DISPONIBLE"
                })

    # Reserved
    reserved = db.query(models.Booking).filter(
        models.Booking.FECHA >= today).filter(models.Booking.FECHA <= end).all()

    # Filter booking if exist on reserved list
    filtered = []
    for b in booking:
        for r in reserved:
            if r.COD_PRODUCTO == b['COD_PRODUCTO'] and r.FECHA == b['FECHA'] and r.HORA_INGRESO == b['HORA_INGRESO']:
                b['ESTADO'] = "RESERVADO"
        filtered.append(b)

    return filtered


@app.post('/bookings/create', response_model=schemas.CreateBooking)
def create_booking(entrada: schemas.CreateBooking, db: Session = Depends(get_db)):
    booking = models.Booking(
        FECHA=entrada.FECHA,
        HORA_INGRESO=entrada.HORA_INGRESO,
        COD_PRODUCTO=entrada.COD_PRODUCTO,
        PRECIO_UNIDAD=entrada.PRECIO_UNIDAD,
        ESTADO=entrada.ESTADO,
        NRO_CLIENTE=entrada.NRO_CLIENTE,
        CANTIDAD=entrada.CANTIDAD)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

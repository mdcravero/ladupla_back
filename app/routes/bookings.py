from typing import List
from fastapi import APIRouter, status, HTTPException
import models
import schemas
from db.conexion import *
from sqlalchemy.orm import Session
from fastapi.params import Depends
from datetime import date, timedelta

booking = APIRouter(tags=['Bookings'])


@booking.get('/bookings/', tags=['Bookings'], response_model=List[schemas.Booking])
def show_bookings(db: Session = Depends(get_db)):
    bookings = db.query(models.Booking).all()
    return bookings


@booking.get('/bookings/available', tags=['Bookings'], response_model=List[schemas.ShowBooking])
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


@booking.post('/bookings/create', response_model=schemas.CreateBooking)
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

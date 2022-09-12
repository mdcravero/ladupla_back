from typing import List
from fastapi import status, HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from . import models, schemas
from .database import get_db, engine
from sqlalchemy.orm import Session
from fastapi.params import Depends
from .hashing import Hash
from datetime import date, timedelta, datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='test FastAPI',
              description='Backend App La Dupla',
              version='1.0')

origins = [
    # "http://localhost",
    "http://localhost:8080",
    # "http://localhost:8000",
    # "http://172.18.0.4:8080",
    '*'

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


@app.get('/users/', tags=['User'], response_model=List[schemas.User])
def show_users(db: Session = Depends(get_db)):
    usuarios = db.query(models.User).all()
    return usuarios


@app.post('/users/', tags=['User'], response_model=schemas.User)
def create_users(entrada: schemas.User, db: Session = Depends(get_db)):
    usuario = models.User(
        EMAIL=entrada.EMAIL, PASSWORD=Hash.bcrypt(entrada.PASSWORD))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@app.post('/login', tags=['Login'], response_model=schemas.Login)
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


@app.get('/bookings/made', tags=['Bookings'])
def made_bookings(db: Session = Depends(get_db)):

    bookings = db.query(models.Booking).filter_by(
        ESTADO='RESERVADA').all()

    bookings_made = []
    DESC = ''
    for b in bookings:
        if b.COD_PRODUCTO == 12:
            DESC = 'Cancha 1'
        elif b.COD_PRODUCTO == 14:
            DESC = 'Cancha 2'
        elif b.COD_PRODUCTO == 15:
            DESC = 'Cancha 3'
        elif b.COD_PRODUCTO == 22:
            DESC = 'Cancha 4'
        bookings_made.append({
            'RESERVA': b.NRO_RESERVA,
            # Utilizo la función strptime para cambiar el formato de la fecha
            'FECHA': datetime.strptime(str(b.FECHA), '%Y-%m-%d').strftime('%d/%m/%y'),
            'FECHA_DATE': b.FECHA,
            'CLIENTE': b.NRO_CLIENTE,
            'HORA_INGRESO': b.HORA_INGRESO,
            'PRECIO_UNIDAD': b.PRECIO_UNIDAD,
            'CANCHA': DESC
        })

    return bookings_made


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
            if r.COD_PRODUCTO == b['COD_PRODUCTO'] and r.FECHA == b['FECHA'] and r.HORA_INGRESO == b['HORA_INGRESO'] and r.ESTADO != 'DISPONIBLE' and r.ESTADO != 'CANCELADA':
                b['ESTADO'] = "RESERVADA"
        filtered.append(b)

    return filtered


@app.post('/bookings/create', response_model=schemas.CreateBooking, tags=['Bookings'])
def create_booking(entrada: schemas.CreateBooking, db: Session = Depends(get_db)):
    def closing_hour():
        hour = entrada.HORA_INGRESO
        if hour == "18:00":
            c_hour = "19:00"
        elif hour == "19:00":
            c_hour = "20:00"
        elif hour == "21:00":
            c_hour = "22:00"
        elif hour == "22:00":
            c_hour = "23:00"
        elif hour == "23:00":
            c_hour = "24:00"
        return c_hour
    booking = models.Booking(
        FECHA=entrada.FECHA,
        USUARIO_CARGA='APP',
        HORA_INGRESO=entrada.HORA_INGRESO,
        HORA_EGRESO=closing_hour(),
        COD_PRODUCTO=entrada.COD_PRODUCTO,
        PRECIO_UNIDAD=entrada.PRECIO_UNIDAD,
        SUBTOTAL=entrada.PRECIO_UNIDAD,
        IMPORTE_TOTAL=entrada.PRECIO_UNIDAD,
        ESTADO=entrada.ESTADO,
        SALDO_A_COBRAR=entrada.PRECIO_UNIDAD,
        NRO_CLIENTE=entrada.NRO_CLIENTE,
        CANTIDAD=entrada.CANTIDAD)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    closing_hour()
    return booking


@app.put('/bookings/cancel/{nro_reserva}', response_model=schemas.CancelBooking, tags=['Bookings'])
def cancel_booking(nro_reserva: str, db: Session = Depends(get_db)):
    reserva = db.query(models.Booking).filter_by(
        NRO_RESERVA=nro_reserva).first()
    reserva.ESTADO = 'CANCELADA'
    db.commit()
    db.refresh(reserva)
    return reserva

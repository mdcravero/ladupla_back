from typing import Optional
from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    EMAIL: str
    PASSWORD: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    EMAIL: str
    PASSWORD: str

    class Config:
        orm_mode = True


class Booking(BaseModel):
    NRO_RESERVA: int
    FECHA: date
    HORA_INGRESO: str
    HORA_EGRESO: str
    ESTADO: str
    NRO_CLIENTE: int
    USUARIO_CARGA: str
    COD_PRODUCTO: int
    CANTIDAD: float
    PRECIO_UNIDAD: float
    SUBTOTAL: float
    DESCUENTO: float
    IMPORTE_TOTAL: float
    SALDO_A_COBRAR: float

    class Config:
        orm_mode = True


class ShowBooking(BaseModel):
    COD_PRODUCTO: int
    NOMBRE_PRODUCTO: str
    PRECIO_UNIDAD: float
    FECHA: date
    HORA_INGRESO: str
    ESTADO: str

    class Config:
        orm_mode = True


class MadeBooking(BaseModel):  # Reservas Realizadas
    NRO_RESERVA: int
    FECHA: date
    HORA_INGRESO: str
    NRO_CLIENTE: int
    COD_PRODUCTO: int
    PRECIO_UNIDAD: float

    class Config:
        orm_mode = True


class CreateBooking(BaseModel):
    NRO_RESERVA: Optional[int]
    FECHA: date
    HORA_INGRESO: str
    COD_PRODUCTO: int
    PRECIO_UNIDAD: float
    ESTADO: str
    NRO_CLIENTE: int
    CANTIDAD: float

    class Config:
        orm_mode = True


class CancelBooking(BaseModel):
    ESTADO: str

    class Config:
        orm_mode = True


# class User(BaseModel):
#     id:Optional[int]
#     username:str
#     nombre:str
#     rol:str
#     estado:int

#     class Config:
#         orm_mode =True

# class UserUpdate(BaseModel):
#     nombre: str

#     class Config:
#         orm_mode = True

# class Respuesta(BaseModel):
#     mensaje: str

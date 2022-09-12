from sqlalchemy import Column, Integer, String, Date, Numeric
from .database import Base


# class User(Base):
#     __tablename__ = 'USUARIOS'

#     USUARIO = Column("USUARIO", String, primary_key=True)
#     NOMBRE = Column("NOMBRE", String)
#     APELLIDO = Column("APELLIDO", String)
#     PASSWORD = Column("PASSWORD", String)
#     FECHA_ALTA = Column("FECHA_ALTA", Date)
#     FECHA_BAJA = Column("FECHA_BAJA", Date)
#     EMAIL = Column("EMAIL", String)
#     ROL = Column("ROL", String)

# En SQLServer la tabla se llama Clientes, pero para en la APP funcionaría como User
class User(Base):
    __tablename__ = 'CLIENTES'

    NRO_CLIENTE = Column("NRO_CLIENTE", Integer, primary_key=True)
    NOMBRE = Column("NOMBRE", String)
    APELLIDO = Column("APELLIDO", String)
    TELEFONO = Column("TELEFONO", String)
    PASSWORD = Column("PASSWORD", String)
    CALLE = Column("CALLE", String)
    NUMERO = Column("NUMERO", Integer)
    BARRIO = Column("BARRIO", String)
    CODIGO_POSTAL = Column("CODIGO_POSTAL", String)
    NUMERO = Column("NUMERO", Integer)
    DNI = Column("DNI", Integer)
    EMAIL = Column("EMAIL", String)


class Booking(Base):
    __tablename__ = 'RESERVAS'

    NRO_RESERVA = Column('NRO_RESERVA', Integer, primary_key=True)
    FECHA = Column('FECHA', Date)
    HORA_INGRESO = Column('HORA_INGRESO', String)
    HORA_EGRESO = Column('HORA_EGRESO', String)
    ESTADO = Column('ESTADO', String)
    NRO_CLIENTE = Column('NRO_CLIENTE', Integer)
    USUARIO_CARGA = Column('USUARIO_CARGA', String)
    COD_PRODUCTO = Column('COD_PRODUCTO', Integer)
    CANTIDAD = Column('CANTIDAD', Numeric)
    PRECIO_UNIDAD = Column('PRECIO_UNIDAD', Numeric)
    SUBTOTAL = Column('SUBTOTAL', Numeric)
    DESCUENTO = Column('DESCUENTO', Numeric)
    IMPORTE_TOTAL = Column('IMPORTE_TOTAL', Numeric)
    SALDO_A_COBRAR = Column('SALDO_A_COBRAR', Numeric)


class Products(Base):
    __tablename__ = 'PRODUCTOS'

    COD_PRODUCTO = Column('COD_PRODUCTO', Integer, primary_key=True)
    DESCRIPCION = Column('DESCRIPCION', String)
    FECHA_ALTA = Column('FECHA_ALTA', Date)
    ESTADO = Column('ESTADO', String)
    TIPO = Column('TIPO', String)
    PRECIO_UNIDAD = Column('PRECIO_UNIDAD', Numeric)
    MUEVE_STOCK = Column('MUEVE_STOCK', String)
    HABILITADO = Column('HABILITADO', String)
    STOCK = Column('STOCK', Integer)

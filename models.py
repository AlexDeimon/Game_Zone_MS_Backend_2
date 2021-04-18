from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
import datetime
from .db_connection import Base, engine

class AdminInDB(Base):
    __tablename__ = "admins"
    username = Column(String(50), primary_key=True, unique=True)
    password = Column(String(50))
    email = Column(String(50))

class ClientInDB(Base):
    __tablename__ = "clientes"
    id_cliente = Column(String(50), primary_key=True, unique=True)
    nombre_cliente = Column(String(50))
    email = Column(String(50))
    telefono = Column(String(50))
    direccion = Column(String(50))

class ProductInDB(Base):
    __tablename__ = "productos"
    id_producto = Column(String(50), primary_key=True, unique=True)
    nombre_producto = Column(String(50))
    precio = Column(Integer)
    cantidad_disponible = Column(Integer)
    
class CompraInDB(Base):
    __tablename__ = "compras"
    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(String(50), ForeignKey("clientes.id_cliente"))
    id_producto = Column(String(50), ForeignKey("productos.id_producto"))
    metodo_pago = Column(String(50))
    fecha_compra = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion_compra = Column(DateTime, default=datetime.datetime.utcnow)

class EnvioInDB(Base):
    __tablename__ = "envios"
    id_envio = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey("compras.id_compra"))
    fecha_envio = Column(DateTime)
    fecha_recibido = Column(DateTime)

Base.metadata.create_all(bind=engine)
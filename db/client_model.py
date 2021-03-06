from sqlalchemy import Column, String, Boolean
from .db_connection import Base, engine

class ClientInDB(Base):
    __tablename__ = "clientes"
    id_cliente = Column(String(50), primary_key = True, unique = True)
    nombre_cliente = Column(String(50))
    email = Column(String(50))
    telefono = Column(String(50))
    direccion = Column(String(50))
    estado = Column(Boolean, default = True)

Base.metadata.create_all(bind = engine)
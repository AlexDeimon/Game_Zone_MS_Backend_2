from sqlalchemy import Column, String, Integer
from .db_connection import Base, engine

class ProductInDB(Base):
    __tablename__ = "productos"
    id_producto = Column(String(50), primary_key=True, unique=True)
    nombre_producto = Column(String(50))
    precio = Column(Integer)
    cantidad_disponible = Column(Integer)

Base.metadata.create_all(bind=engine)
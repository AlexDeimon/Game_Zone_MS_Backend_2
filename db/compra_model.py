from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import datetime
from .db_connection import Base, engine

class CompraInDB(Base):
    __tablename__ = "compras"
    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(String(50), ForeignKey("clientes.id_cliente"))
    id_producto = Column(String(50), ForeignKey("productos.id_producto"))
    metodo_pago = Column(String(50))
    fecha_compra = Column(DateTime, default=datetime.datetime.utcnow)
    fecha_actualizacion_compra = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)
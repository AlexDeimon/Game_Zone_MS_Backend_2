from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
import datetime
from .db_connection import Base, engine


class EnvioInDB(Base):
    __tablename__ = "envios"
    id_envio = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey("compras.id_compra"))
    fecha_envio = Column(DateTime)
    fecha_recibido = Column(DateTime)

Base.metadata.create_all(bind=engine)
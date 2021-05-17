from sqlalchemy import Column, String, Integer, ForeignKey, Date, Boolean
import datetime
from .db_connection import Base, engine


class EnvioInDB(Base):
    __tablename__ = "envios"
    id_envio = Column(Integer, primary_key=True, autoincrement=True)
    id_compra = Column(Integer, ForeignKey("compras.id_compra"))
    fecha_envio = Column(Date)
    fecha_recibido = Column(Date)
    estado = Column(Boolean(), default=True)

Base.metadata.create_all(bind=engine)
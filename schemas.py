from pydantic import BaseModel
from datetime import datetime
from typing import List

class AdminIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class Client(BaseModel):
    id_cliente: str
    nombre_cliente: str
    email: str
    telefono: str
    direccion: str

    class Config:
        orm_mode = True

class ClientUpdate(BaseModel):
    nombre_cliente: str
    email: str
    telefono: str
    direccion: str

    class Config:
        orm_mode = True

class Product(BaseModel):
    id_producto: str
    nombre_producto: str
    precio: int
    cantidad_disponible: int

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    nombre_producto: str
    precio: int
    cantidad_disponible: int

    class Config:
        orm_mode = True

class CompraIn(BaseModel):
    id_cliente: str
    id_producto: str
    metodo_pago:str

    class Config:
        orm_mode = True

class CompraOut(BaseModel):
    id_compra: int
    id_cliente: str
    id_producto: str
    metodo_pago:str
    fecha_compra: datetime
    fecha_actualizacion_compra: datetime

    class Config:
        orm_mode = True

class CompraUpdate(BaseModel):
    id_cliente: str
    id_producto: str
    metodo_pago:str
    fecha_actualizacion_compra: datetime

    class Config:
        orm_mode = True

class EnvioIn(BaseModel):
    id_compra: int
    fecha_envio: datetime
    fecha_recibido: datetime

    class Config:
        orm_mode = True
    
class EnvioOut(BaseModel):
    id_envio: int
    id_compra: int
    fecha_envio: datetime
    fecha_recibido: datetime

    class Config:
        orm_mode = True

class EnvioUpdate(BaseModel):
    id_compra: int
    fecha_envio: datetime
    fecha_recibido: datetime

    class Config:
        orm_mode = True

class respuesta(BaseModel):
    mensaje:str
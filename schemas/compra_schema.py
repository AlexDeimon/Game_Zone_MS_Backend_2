from pydantic import BaseModel
from datetime import datetime

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
from pydantic import BaseModel
from datetime import date

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
    fecha_compra: date
    fecha_actualizacion_compra: date

    class Config:
        orm_mode = True

class CompraUpdate(BaseModel):
    id_cliente: str
    id_producto: str
    metodo_pago:str
    fecha_actualizacion_compra: date

    class Config:
        orm_mode = True
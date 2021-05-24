from pydantic import BaseModel
from datetime import date

class EnvioIn(BaseModel):
    id_compra: int
    fecha_envio: date
    fecha_recibido: date

    class Config:
        orm_mode = True
    
class EnvioOut(BaseModel):
    id_envio: int
    id_compra: int
    fecha_envio: date
    fecha_recibido: date

    class Config:
        orm_mode = True
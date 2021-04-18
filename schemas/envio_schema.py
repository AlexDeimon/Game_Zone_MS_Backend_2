from pydantic import BaseModel
from datetime import datetime

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
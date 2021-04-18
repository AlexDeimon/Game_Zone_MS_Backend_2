from pydantic import BaseModel

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
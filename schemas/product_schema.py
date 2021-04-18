from pydantic import BaseModel

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
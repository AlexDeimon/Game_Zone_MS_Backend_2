from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.product_model import ProductInDB
from schemas.product_schema import Product, ProductUpdate
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/producto/",response_model=Product)
def new_products(entrada:Product,db:Session=Depends(get_db)):
    producto = ProductInDB(id_producto=entrada.id_producto, nombre_producto=entrada.nombre_producto, precio=entrada.precio, cantidad_disponible=entrada.cantidad_disponible)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@router.get("/productos/",response_model=List[Product])
def all_products(db:Session=Depends(get_db)):
    productos=db.query(ProductInDB).all()
    return productos

@router.get("/buscar/producto/{id_producto}",response_model=Product)
def search_products(id_producto:str,db:Session=Depends(get_db)):
    productos=db.query(ProductInDB).filter(ProductInDB.id_producto == id_producto).first()
    return productos

@router.put("/actualizar/producto/{id_producto}/",response_model=Product)
def update_products(id_producto:str,entrada:ProductUpdate,db:Session=Depends(get_db)):
    producto = db.query(ProductInDB).filter_by(id_producto=id_producto).first()
    producto.nombre_producto=entrada.nombre_producto
    producto.precio=entrada.precio
    producto.cantidad_disponible=entrada.cantidad_disponible
    db.commit()
    db.refresh(producto)
    return producto

@router.delete("/eliminar/producto/{id_producto}/",response_model=respuesta)
def delete_products(id_producto:str,db:Session=Depends(get_db)):
    producto = db.query(ProductInDB).filter_by(id_producto=id_producto).first()
    db.delete(producto)
    db.commit()
    Respuesta = respuesta(mensaje="Producto eliminado exitosamente")
    return Respuesta
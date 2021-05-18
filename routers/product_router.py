from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.product_model import ProductInDB
from schemas.product_schema import Product, ProductUpdate
from db.compra_model import CompraInDB
from db.envio_model import EnvioInDB
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/producto/", response_model = Product, tags = ["producto"])
def new_products(entrada: Product, db: Session = Depends(get_db)):
    try:
        producto = ProductInDB(id_producto = entrada.id_producto, nombre_producto = entrada.nombre_producto, precio = entrada.precio, cantidad_disponible = entrada.cantidad_disponible)
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto
    except:
        raise HTTPException(status_code = 404, detail = "El producto ya existe")

@router.get("/productos/", response_model = List[Product], tags=["producto"])
def all_products(db: Session = Depends(get_db)):
    productos = db.query(ProductInDB).order_by(ProductInDB.id_producto).filter(ProductInDB.estado == True).all()
    return productos

@router.get("/buscar/producto/{id_producto}/", response_model = Product, tags = ["producto"])
def search_products(id_producto: str, db: Session = Depends(get_db)):
    producto = db.query(ProductInDB).filter(ProductInDB.id_producto == id_producto, ProductInDB.estado == True).first()
    if producto == None:
        raise HTTPException(status_code = 404, detail = "El producto no existe")
    else:
        return producto

@router.put("/actualizar/producto/{id_producto}/", response_model = Product, tags = ["producto"])
def update_products(id_producto: str, entrada: ProductUpdate, db: Session = Depends(get_db)):
    try:
        producto = db.query(ProductInDB).filter(ProductInDB.id_producto == id_producto, ProductInDB.estado == True).first()
        producto.nombre_producto = entrada.nombre_producto
        producto.precio = entrada.precio
        producto.cantidad_disponible = entrada.cantidad_disponible
        producto.estado = True
        db.commit()
        db.refresh(producto)
        return producto
    except:
        raise HTTPException(status_code = 404, detail = "El producto no existe")

@router.delete("/eliminar/producto/{id_producto}/",response_model = respuesta, tags=["producto"])
def delete_products(id_producto: str, db: Session = Depends(get_db)):
    producto = db.query(ProductInDB).filter(ProductInDB.id_producto == id_producto, ProductInDB.estado == True).first()
    if producto == None:
        raise HTTPException(status_code = 404, detail = "El producto no existe")
    else:
        compras = db.query(CompraInDB).filter(CompraInDB.id_producto == producto.id_producto, CompraInDB.estado == True).all()
        if compras == None:
            producto.estado = False
            db.commit()
            db.refresh(producto)
            Respuesta = respuesta(mensaje = "Producto eliminado exitosamente")
            return Respuesta
        else:
            producto.estado = False
            db.commit()
            db.refresh(producto)
            Respuesta = respuesta(mensaje = "Producto eliminado exitosamente")
            for compra in compras:
                envio = db.query(EnvioInDB).filter(EnvioInDB.id_compra == compra.id_compra, EnvioInDB.estado == True).first()
                if envio == None:
                    compra.estado = False
                    db.commit()
                    db.refresh(compra)
                else:
                    compra.estado = False
                    envio.estado = False
                    db.commit()
                    db.refresh(compra)
                    db.refresh(envio)
                    Respuesta = respuesta(mensaje = "Producto eliminado exitosamente")
            return Respuesta
from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.compra_model import CompraInDB
from schemas.compra_schema import CompraIn, CompraOut, CompraUpdate
from db.product_model import ProductInDB
from db.envio_model import EnvioInDB
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nueva/compra/", response_model = CompraOut, tags = ["compra"])
def new_compra(entrada: CompraIn, db: Session = Depends(get_db)):
    try:
        compra = CompraInDB(id_cliente = entrada.id_cliente, id_producto = entrada.id_producto, metodo_pago = entrada.metodo_pago)
        producto = db.query(ProductInDB).filter(ProductInDB.id_producto == entrada.id_producto, ProductInDB.estado == True).first()
        if producto.cantidad_disponible > 0:
            producto.cantidad_disponible = producto.cantidad_disponible - 1
            db.add(compra)
            db.commit()
            db.refresh(compra)
            db.refresh(producto)
            return compra
        else:
            raise HTTPException(status_code = 404, detail = "El producto está agotado")
    except:
        raise HTTPException(status_code = 404, detail = "Error: posibles causas: 1. La compra ya existe. 2. El id de cliente y/o producto no existen. 3. El producto está agotado")

@router.get("/compras/", response_model = List[CompraOut], tags = ["compra"])
def all_compras(db:Session = Depends(get_db)):
    compras = db.query(CompraInDB).order_by(CompraInDB.id_compra).filter(CompraInDB.estado == True).all()
    return compras

@router.get("/buscar/compra/{id_compra}/", response_model = CompraOut, tags = ["compra"])
def search_compra(id_compra: int, db: Session = Depends(get_db)):
    compra = db.query(CompraInDB).filter(CompraInDB.id_compra == id_compra, CompraInDB.estado == True).first()
    if compra == None:
        raise HTTPException(status_code = 404, detail = "La compra no existe")
    else:
        return compra

@router.put("/actualizar/compra/{id_compra}/", response_model = CompraOut, tags = ["compra"])
def update_compra(id_compra: int, entrada: CompraUpdate, db: Session = Depends(get_db)):
    try:
        compra = db.query(CompraInDB).filter(CompraInDB.id_compra == id_compra, CompraInDB.estado == True).first()
        compra.id_cliente = entrada.id_cliente
        compra.id_producto = entrada.id_producto
        compra.metodo_pago = entrada.metodo_pago
        compra.fecha_actualizacion_compra = entrada.fecha_actualizacion_compra
        compra.estado = True
        db.commit()
        db.refresh(compra)
        return compra
    except:
        raise HTTPException(status_code = 404,detail = "La compra no existe")

@router.delete("/eliminar/compra/{id_compra}/", response_model = respuesta, tags = ["compra"])
def delete_compra(id_compra: int, db: Session = Depends(get_db)):
    compra = db.query(CompraInDB).filter(CompraInDB.id_compra == id_compra, CompraInDB.estado == True).first()
    if compra == None:
        raise HTTPException(status_code = 404, detail = "La compra no existe")
    else:
        envio = db.query(EnvioInDB).filter(EnvioInDB.id_compra == id_compra, EnvioInDB.estado == True).first()
        producto = db.query(ProductInDB).filter(ProductInDB.id_producto == compra.id_producto, ProductInDB.estado == True).first()
        if envio == None:
            compra.estado = False
            producto.cantidad_disponible = producto.cantidad_disponible + 1
            db.commit()
            db.refresh(compra)
            db.refresh(producto)
            Respuesta = respuesta(mensaje = "Compra eliminada exitosamente")
            return Respuesta
        else:
            compra.estado = False
            envio.estado = False
            producto.cantidad_disponible = producto.cantidad_disponible + 1
            db.commit()
            db.refresh(compra)
            db.refresh(envio)
            db.refresh(producto)
            Respuesta = respuesta(mensaje = "Compra eliminada exitosamente")
            return Respuesta
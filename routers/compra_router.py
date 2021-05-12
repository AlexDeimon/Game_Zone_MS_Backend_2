from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.compra_model import CompraInDB
from schemas.compra_schema import CompraIn, CompraOut, CompraUpdate
from db.envio_model import EnvioInDB
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nueva/compra/",response_model=CompraOut)
def new_compra(entrada:CompraIn,db:Session=Depends(get_db)):
    try:
        compra = CompraInDB(id_cliente=entrada.id_cliente,id_producto=entrada.id_producto, metodo_pago=entrada.metodo_pago)
        db.add(compra)
        db.commit()
        db.refresh(compra)
        return compra
    except:
        raise HTTPException(status_code=404,detail="La compra ya existe")

@router.get("/compras/",response_model=List[CompraOut])
def all_compras(db:Session=Depends(get_db)):
    compras=db.query(CompraInDB).all()
    return compras

@router.get("/buscar/compra/{id_compra}",response_model=CompraOut)
def search_compra(id_compra:int,db:Session=Depends(get_db)):
    compra=db.query(CompraInDB).filter(CompraInDB.id_compra == id_compra).first()
    if compra==None:
        raise HTTPException(status_code=404,detail="La compra no existe")
    else:
        return compra

@router.put("/actualizar/compra/{id_compra}/",response_model=CompraOut)
def update_compra(id_compra:int,entrada:CompraUpdate,db:Session=Depends(get_db)):
    try:
        compra = db.query(CompraInDB).filter_by(id_compra=id_compra).first()
        compra.id_cliente=entrada.id_cliente
        compra.id_producto=entrada.id_producto
        compra.metodo_pago=entrada.metodo_pago
        compra.fecha_actualizacion_compra=entrada.fecha_actualizacion_compra
        db.commit()
        db.refresh(compra)
        return compra
    except:
        raise HTTPException(status_code=404,detail="La compra no existe")

@router.delete("/eliminar/compra/{id_compra}/",response_model=respuesta)
def delete_compra(id_compra:int,db:Session=Depends(get_db)):
    compra = db.query(CompraInDB).filter_by(id_compra=id_compra).first()
    envio = db.query(EnvioInDB).filter_by(id_compra=id_compra).first()
    if compra==None:
        raise HTTPException(status_code=404,detail="La compra no existe")
    else:
        db.delete(compra)
        db.delete(envio)
        db.commit()
        Respuesta = respuesta(mensaje="Compra eliminada exitosamente")
        return Respuesta
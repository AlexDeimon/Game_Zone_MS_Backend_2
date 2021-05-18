from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.envio_model import EnvioInDB
from schemas.envio_schema import EnvioIn, EnvioOut, EnvioUpdate
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/envio/", response_model = EnvioOut, tags = ["envios"])
def new_envio(entrada: EnvioIn, db:Session = Depends(get_db)):
    try:
        envio = EnvioInDB(id_compra = entrada.id_compra, fecha_envio = entrada.fecha_envio, fecha_recibido = entrada.fecha_recibido)
        db.add(envio)
        db.commit()
        db.refresh(envio)
        return envio
    except:
        raise HTTPException(status_code = 404, detail = "Error: posibles causas: 1. El envio ya existe. 2. El id de compra no existe")

@router.get("/envios/", response_model = List[EnvioOut], tags=["envios"])
def all_envios(db:Session = Depends(get_db)):
    envios = db.query(EnvioInDB).order_by(EnvioInDB.id_envio).filter(EnvioInDB.estado == True).all()
    return envios

@router.get("/buscar/envio/{id_envio}/", response_model = EnvioOut, tags = ["envios"])
def search_envio(id_envio: int, db: Session = Depends(get_db)):
    envio = db.query(EnvioInDB).filter(EnvioInDB.id_envio == id_envio, EnvioInDB.estado == True).first()
    if envio == None:
        raise HTTPException(status_code = 404, detail = "El envio no existe")
    else:
        return envio

@router.put("/actualizar/envio/{id_envio}/", response_model = EnvioOut, tags = ["envios"])
def update_envio(id_envio: int, entrada: EnvioUpdate, db: Session = Depends(get_db)):
    try:
        envio = db.query(EnvioInDB).filter(EnvioInDB.id_envio == id_envio, EnvioInDB.estado == True).first()
        envio.id_compra = entrada.id_compra
        envio.fecha_envio = entrada.fecha_envio
        envio.fecha_recibido = entrada.fecha_recibido
        envio.estado = True
        db.commit()
        db.refresh(envio)
        return envio
    except:
        raise HTTPException(status_code = 404, detail = "El envio no existe")

@router.delete("/eliminar/envio/{id_envio}/", response_model = respuesta, tags = ["envios"])
def delete_envio(id_envio: int, db: Session = Depends(get_db)):
    envio = db.query(EnvioInDB).filter(EnvioInDB.id_envio == id_envio, EnvioInDB.estado == True).first()
    if envio == None:
        raise HTTPException(status_code = 404, detail = "El envio no existe")
    else:
        envio.estado = False
        db.commit()
        db.refresh(envio)
        Respuesta = respuesta(mensaje = "Envio eliminado exitosamente")
        return Respuesta

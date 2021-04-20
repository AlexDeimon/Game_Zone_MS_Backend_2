from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.envio_model import EnvioInDB
from schemas.envio_schema import EnvioIn, EnvioOut, EnvioUpdate
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/envio/",response_model=EnvioOut)
def new_envio(entrada:EnvioIn,db:Session=Depends(get_db)):
    try:
        envio = EnvioInDB(id_compra=entrada.id_compra, fecha_envio=entrada.fecha_envio, fecha_recibido=entrada.fecha_recibido)
        db.add(envio)
        db.commit()
        db.refresh(envio)
        return envio
    except:
        raise HTTPException(status_code=404,detail="El envio ya existe")

@router.get("/envios/",response_model=List[EnvioOut])
def all_envios(db:Session=Depends(get_db)):
    envios=db.query(EnvioInDB).all()
    return envios

@router.get("/buscar/envio/{id_envio}",response_model=EnvioOut)
def search_envio(id_envio:int,db:Session=Depends(get_db)):
    envio=db.query(EnvioInDB).filter(EnvioInDB.id_envio == id_envio).first()
    if envio==None:
        raise HTTPException(status_code=404,detail="El envio no existe")
    else:
        return envio

@router.put("/actualizar/envio/{id_envio}/",response_model=EnvioOut)
def update_envio(id_envio:int,entrada:EnvioUpdate,db:Session=Depends(get_db)):
    try:
        envio = db.query(EnvioInDB).filter_by(id_envio=id_envio).first()
        envio.id_compra=entrada.id_compra
        envio.fecha_envio=entrada.fecha_envio
        envio.fecha_recibido=entrada.fecha_recibido
        db.commit()
        db.refresh(envio)
        return envio
    except:
        raise HTTPException(status_code=404,detail="El envio no existe")

@router.delete("/eliminar/envio/{id_envio}/",response_model=respuesta)
def delete_envio(id_envio:int,db:Session=Depends(get_db)):
    envio = db.query(EnvioInDB).filter_by(id_envio=id_envio).first()
    if envio==None:
        raise HTTPException(status_code=404,detail="El envio no existe")
    else:
        db.delete(envio)
        db.commit()
        Respuesta = respuesta(mensaje="Envio eliminado exitosamente")
        return Respuesta

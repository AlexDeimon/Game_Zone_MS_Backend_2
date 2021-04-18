from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.client_model import ClientInDB
from schemas.client_schema import Client, ClientUpdate
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/cliente/",response_model=Client)
def new_clients(entrada:Client,db:Session=Depends(get_db)):
    cliente = ClientInDB(id_cliente=entrada.id_cliente, nombre_cliente=entrada.nombre_cliente, email=entrada.email, telefono=entrada.telefono, direccion=entrada.direccion)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.get("/clientes/",response_model=List[Client])
def all_clients(db:Session=Depends(get_db)):
    clientes=db.query(ClientInDB).all()
    return clientes

@router.get("/buscar/cliente/{id_cliente}",response_model=Client)
def search_clients(id_cliente:str,db:Session=Depends(get_db)):
    clientes=db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente).first()
    return clientes

@router.put("/actualizar/cliente/{id_cliente}/",response_model=Client)
def update_clients(id_cliente:str,entrada:ClientUpdate,db:Session=Depends(get_db)):
    cliente = db.query(ClientInDB).filter_by(id_cliente=id_cliente).first()
    cliente.nombre_cliente=entrada.nombre_cliente
    cliente.email=entrada.email
    cliente.telefono=entrada.telefono
    cliente.direccion=entrada.direccion
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/eliminar/cliente/{id_cliente}/",response_model=respuesta)
def delete_clients(id_cliente:str,db:Session=Depends(get_db)):
    cliente = db.query(ClientInDB).filter_by(id_cliente=id_cliente).first()
    db.delete(cliente)
    db.commit()
    Respuesta = respuesta(mensaje="Cliente eliminado exitosamente")
    return Respuesta
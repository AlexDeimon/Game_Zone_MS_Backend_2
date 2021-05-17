from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.client_model import ClientInDB
from schemas.client_schema import Client, ClientUpdate
from db.compra_model import CompraInDB
from db.envio_model import EnvioInDB
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/cliente/",response_model = Client,tags=["cliente"])
def new_clients(entrada:Client,db:Session = Depends(get_db)):
    try:
        cliente = ClientInDB(id_cliente = entrada.id_cliente, nombre_cliente = entrada.nombre_cliente, email = entrada.email, telefono = entrada.telefono, direccion = entrada.direccion)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except:
        raise HTTPException(status_code = 404,detail = "El cliente ya existe")

@router.get("/clientes/",response_model = List[Client],tags=["cliente"])
def all_clients(db:Session = Depends(get_db)):
    clientes = db.query(ClientInDB).filter(ClientInDB.estado==True).all()
    return clientes

@router.get("/buscar/cliente/{id_cliente}/",response_model = Client,tags=["cliente"])
def search_clients(id_cliente:str,db:Session = Depends(get_db)):
    cliente = db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente, ClientInDB.estado == True).first()
    if cliente == None:
        raise HTTPException(status_code = 404,detail = "El cliente no existe")
    else:
        return cliente

@router.put("/actualizar/cliente/{id_cliente}/",response_model = Client,tags=["cliente"])
def update_clients(id_cliente:str,entrada:ClientUpdate,db:Session = Depends(get_db)):
    try:
        cliente = db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente, ClientInDB.estado == True).first()
        cliente.nombre_cliente = entrada.nombre_cliente
        cliente.email = entrada.email
        cliente.telefono = entrada.telefono
        cliente.direccion = entrada.direccion
        cliente.estado = True
        db.commit()
        db.refresh(cliente)
        return cliente
    except:
        raise HTTPException(status_code = 404,detail = "El cliente no existe")

@router.delete("/eliminar/cliente/{id_cliente}/",response_model=respuesta,tags=["cliente"])
def delete_clients(id_cliente:str,db:Session = Depends(get_db)):
    cliente = db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente, ClientInDB.estado == True).first()
    compra = db.query(CompraInDB).filter(CompraInDB.id_cliente == id_cliente, CompraInDB.estado == True).first()
    envio = db.query(EnvioInDB).filter(EnvioInDB.id_compra == CompraInDB.id_compra, EnvioInDB.estado == True).first()
    if cliente == None:
        raise HTTPException(status_code = 404,detail = "El cliente no existe")
    else:
        cliente.estado = False
        compra.estado = False
        envio.estado = False
        db.commit()
        db.refresh(cliente)
        db.refresh(compra)
        db.refresh(envio)
        Respuesta = respuesta(mensaje = "Cliente eliminado exitosamente")
        return Respuesta
        
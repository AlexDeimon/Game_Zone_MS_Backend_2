from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.client_model import ClientInDB
from schemas.client_schema import Client
from db.product_model import ProductInDB
from db.compra_model import CompraInDB
from db.envio_model import EnvioInDB
from schemas.respuesta import respuesta

router = APIRouter()

@router.post("/nuevo/cliente/", response_model = Client, tags = ["cliente"])
def new_clients(entrada: Client, db: Session = Depends(get_db)):
    try:
        cliente = ClientInDB(id_cliente = entrada.id_cliente, nombre_cliente = entrada.nombre_cliente, email = entrada.email, telefono = entrada.telefono, direccion = entrada.direccion)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    except:
        raise HTTPException(status_code = 404,detail = "El cliente ya existe")

@router.get("/clientes/", response_model = List[Client], tags = ["cliente"])
def all_clients(db: Session = Depends(get_db)):
    clientes = db.query(ClientInDB).order_by(ClientInDB.id_cliente).filter(ClientInDB.estado == True).all()
    return clientes

@router.get("/buscar/cliente/{id_cliente}/", response_model = Client, tags = ["cliente"])
def search_clients(id_cliente: str, db: Session = Depends(get_db)):
    cliente = db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente, ClientInDB.estado == True).first()
    if cliente == None:
        raise HTTPException(status_code = 404, detail = "El cliente no existe")
    else:
        return cliente

@router.put("/actualizar/cliente/", response_model = Client, tags = ["cliente"])
def update_clients(client: Client, db: Session = Depends(get_db)):
    cliente = db.query(ClientInDB).get(client.id_cliente)

    if cliente.estado == False or cliente == None:
        raise HTTPException(status_code = 404, detail = "El cliente no existe") 

    cliente.nombre_cliente = client.nombre_cliente
    cliente.email = client.email
    cliente.telefono = client.telefono
    cliente.direccion = client.direccion

    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/eliminar/cliente/{id_cliente}/", response_model = respuesta, tags = ["cliente"])
def delete_clients(id_cliente: str, db: Session = Depends(get_db)):
    cliente = db.query(ClientInDB).filter(ClientInDB.id_cliente == id_cliente, ClientInDB.estado == True).first()
    if cliente == None:
        raise HTTPException(status_code = 404, detail = "El cliente no existe")
    else:
        compras = db.query(CompraInDB).filter(CompraInDB.id_cliente == cliente.id_cliente, CompraInDB.estado == True).all()
        if compras == None:
            cliente.estado = False
            db.commit()
            db.refresh(cliente)
            Respuesta = respuesta(mensaje = "Cliente eliminado exitosamente")
            return Respuesta
        else:
            cliente.estado = False
            db.commit()
            db.refresh(cliente)
            Respuesta = respuesta(mensaje = "Cliente eliminado exitosamente")
            for compra in compras:
                envio = db.query(EnvioInDB).filter(EnvioInDB.id_compra == compra.id_compra, EnvioInDB.estado == True).first()
                producto = db.query(ProductInDB).filter(ProductInDB.id_producto == compra.id_producto, ProductInDB.estado == True).first()
                if envio == None:
                    compra.estado = False
                    producto.cantidad_disponible = producto.cantidad_disponible + 1
                    db.commit()
                    db.refresh(compra)
                    db.refresh(producto)
                else:
                    compra.estado = False
                    envio.estado = False
                    producto.cantidad_disponible = producto.cantidad_disponible + 1
                    db.commit()
                    db.refresh(compra)
                    db.refresh(envio)
                    db.refresh(producto)
            return Respuesta
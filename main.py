from typing import List
from fastapi import FastAPI, Depends, HTTPException
from starlette.responses import RedirectResponse
from .db_connection import SessionLocal
from . import models,schemas
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

######################################## Admin ########################################
@app.post("/admin/auth/")
def auth_admin(admin_in: schemas.AdminIn, db: Session = Depends(get_db)):
    admin_in_db = db.query(models.AdminInDB).get(admin_in.username)
    if admin_in_db == None:
        raise HTTPException(status_code=404,detail="El usuario no existe")
    if admin_in_db.password != admin_in.password:
        raise HTTPException(status_code=403,detail="Error de autenticacion")
    return {"Bienvenido "+admin_in.username}

######################################## Cliente ########################################
@app.post("/nuevo/cliente/",response_model=schemas.Client)
def new_clients(entrada:schemas.Client,db:Session=Depends(get_db)):
    cliente = models.ClientInDB(id_cliente=entrada.id_cliente, nombre_cliente=entrada.nombre_cliente, email=entrada.email, telefono=entrada.telefono, direccion=entrada.direccion)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@app.get("/clientes/",response_model=List[schemas.Client])
def all_clients(db:Session=Depends(get_db)):
    clientes=db.query(models.ClientInDB).all()
    return clientes

@app.get("/buscar/cliente/{id_cliente}",response_model=schemas.Client)
def search_clients(id_cliente:str,db:Session=Depends(get_db)):
    clientes=db.query(models.ClientInDB).filter(models.ClientInDB.id_cliente == id_cliente).first()
    return clientes

@app.put("/actualizar/cliente/{id_cliente}/",response_model=schemas.Client)
def update_clients(id_cliente:str,entrada:schemas.ClientUpdate,db:Session=Depends(get_db)):
    cliente = db.query(models.ClientInDB).filter_by(id_cliente=id_cliente).first()
    cliente.nombre_cliente=entrada.nombre_cliente
    cliente.email=entrada.email
    cliente.telefono=entrada.telefono
    cliente.direccion=entrada.direccion
    db.commit()
    db.refresh(cliente)
    return cliente

@app.delete("/eliminar/cliente/{id_cliente}/",response_model=schemas.respuesta)
def delete_clients(id_cliente:str,db:Session=Depends(get_db)):
    cliente = db.query(models.ClientInDB).filter_by(id_cliente=id_cliente).first()
    db.delete(cliente)
    db.commit()
    Respuesta = schemas.respuesta(mensaje="Cliente eliminado exitosamente")
    return Respuesta

######################################## producto ########################################
@app.post("/nuevo/producto/",response_model=schemas.Product)
def new_products(entrada:schemas.Product,db:Session=Depends(get_db)):
    producto = models.ProductInDB(id_producto=entrada.id_producto, nombre_producto=entrada.nombre_producto, precio=entrada.precio, cantidad_disponible=entrada.cantidad_disponible)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

@app.get("/productos/",response_model=List[schemas.Product])
def all_products(db:Session=Depends(get_db)):
    productos=db.query(models.ProductInDB).all()
    return productos

@app.get("/buscar/producto/{id_producto}",response_model=schemas.Product)
def search_products(id_producto:str,db:Session=Depends(get_db)):
    productos=db.query(models.ProductInDB).filter(models.ProductInDB.id_producto == id_producto).first()
    return productos

@app.put("/actualizar/producto/{id_producto}/",response_model=schemas.Product)
def update_products(id_producto:str,entrada:schemas.ProductUpdate,db:Session=Depends(get_db)):
    producto = db.query(models.ProductInDB).filter_by(id_producto=id_producto).first()
    producto.nombre_producto=entrada.nombre_producto
    producto.precio=entrada.precio
    producto.cantidad_disponible=entrada.cantidad_disponible
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/eliminar/producto/{id_producto}/",response_model=schemas.respuesta)
def delete_products(id_producto:str,db:Session=Depends(get_db)):
    producto = db.query(models.ProductInDB).filter_by(id_producto=id_producto).first()
    db.delete(producto)
    db.commit()
    Respuesta = schemas.respuesta(mensaje="Producto eliminado exitosamente")
    return Respuesta

######################################## compra ########################################
@app.post("/nueva/compra/",response_model=schemas.CompraOut)
def new_compra(entrada:schemas.CompraIn,db:Session=Depends(get_db)):
    compra = models.CompraInDB(id_cliente=entrada.id_cliente,id_producto=entrada.id_producto, metodo_pago=entrada.metodo_pago)
    db.add(compra)
    db.commit()
    db.refresh(compra)
    return compra

@app.get("/compras/",response_model=List[schemas.CompraOut])
def all_compras(db:Session=Depends(get_db)):
    compras=db.query(models.CompraInDB).all()
    return compras

@app.get("/buscar/compra/{id_compra}",response_model=schemas.CompraOut)
def search_compra(id_compra:int,db:Session=Depends(get_db)):
    compras=db.query(models.CompraInDB).filter(models.CompraInDB.id_compra == id_compra).first()
    return compras

@app.put("/actualizar/compra/{id_compra}/",response_model=schemas.CompraOut)
def update_compra(id_compra:int,entrada:schemas.CompraUpdate,db:Session=Depends(get_db)):
    compra = db.query(models.CompraInDB).filter_by(id_compra=id_compra).first()
    compra.id_cliente=entrada.id_cliente
    compra.id_producto=entrada.id_producto
    compra.metodo_pago=entrada.metodo_pago
    compra.fecha_actualizacion_compra=entrada.fecha_actualizacion_compra
    db.commit()
    db.refresh(compra)
    return compra

@app.delete("/eliminar/compra/{id_compra}/",response_model=schemas.respuesta)
def delete_compra(id_compra:str,db:Session=Depends(get_db)):
    compra = db.query(models.CompraInDB).filter_by(id_compra=id_compra).first()
    db.delete(compra)
    db.commit()
    Respuesta = schemas.respuesta(mensaje="Compra eliminada exitosamente")
    return Respuesta

######################################## envio ########################################
@app.post("/nuevo/envio/",response_model=schemas.EnvioOut)
def new_envio(entrada:schemas.EnvioIn,db:Session=Depends(get_db)):
    envio = models.EnvioInDB(id_compra=entrada.id_compra, fecha_envio=entrada.fecha_envio, fecha_recibido=entrada.fecha_recibido)
    db.add(envio)
    db.commit()
    db.refresh(envio)
    return envio

@app.get("/envios/",response_model=List[schemas.EnvioOut])
def all_envios(db:Session=Depends(get_db)):
    envios=db.query(models.EnvioInDB).all()
    return envios

@app.get("/buscar/envio/{id_envio}",response_model=schemas.EnvioOut)
def search_envio(id_envio:int,db:Session=Depends(get_db)):
    envios=db.query(models.EnvioInDB).filter(models.EnvioInDB.id_envio == id_envio).first()
    return envios

@app.put("/actualizar/envio/{id_envio}/",response_model=schemas.EnvioOut)
def update_envio(id_envio:int,entrada:schemas.EnvioUpdate,db:Session=Depends(get_db)):
    envio = db.query(models.EnvioInDB).filter_by(id_envio=id_envio).first()
    envio.id_compra=entrada.id_compra
    envio.fecha_envio=entrada.fecha_envio
    envio.fecha_recibido=entrada.fecha_recibido
    db.commit()
    db.refresh(envio)
    return envio

@app.delete("/eliminar/envio/{id_envio}/",response_model=schemas.respuesta)
def delete_envio(id_envio:str,db:Session=Depends(get_db)):
    envio = db.query(models.EnvioInDB).filter_by(id_envio=id_envio).first()
    db.delete(envio)
    db.commit()
    Respuesta = schemas.respuesta(mensaje="Envio eliminado exitosamente")
    return Respuesta

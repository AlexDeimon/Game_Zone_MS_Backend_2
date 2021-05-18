from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from db.db_connection import get_db
from db.admin_model import AdminInDB
from schemas.admin_schema import AdminIn

router = APIRouter()

@router.post("/admin/auth/", tags = ["user"])
def auth_admin(admin_in: AdminIn, db: Session = Depends(get_db)):
    admin_in_db = db.query(AdminInDB).get(admin_in.username)
    if admin_in_db == None:
        raise HTTPException(status_code = 404, detail = "El usuario no existe")
    if admin_in_db.password != admin_in.password:
        raise HTTPException(status_code = 403, detail = "Error de autenticacion")
    return {"Bienvenido " + admin_in.username}
from sqlalchemy import Column, String
from .db_connection import Base, engine

class AdminInDB(Base):
    __tablename__ = "admins"
    username = Column(String(50), primary_key = True, unique = True)
    password = Column(String(50))
    email = Column(String(50))

Base.metadata.create_all(bind = engine)
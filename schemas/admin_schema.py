from pydantic import BaseModel

class AdminIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
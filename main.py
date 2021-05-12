from fastapi import Depends, FastAPI
from routers.admin_router import router as router_admin
from routers.client_router import router as router_client
from routers.compra_router import router as router_compra
from routers.envio_router import router as router_envio
from routers.product_router import router as router_product

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
origins = [
"http://localhost.tiangolo.com", "https://localhost.tiangolo.com",
"http://localhost", "http://localhost:8080","https://gamezone-ms-app.herokuapp.com"
]
api.add_middleware(
CORSMiddleware, allow_origins=origins,
allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

api.include_router(router_admin)
api.include_router(router_client)
api.include_router(router_product)
api.include_router(router_compra)
api.include_router(router_envio)


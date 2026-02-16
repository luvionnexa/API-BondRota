from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
import models 

from routers import clientes, motoristas, veiculos, pontos, rotas_internas, administradores, horarios_fixos_cliente, reservas


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API BondRota.", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clientes.router)
app.include_router(pontos.router)
app.include_router(veiculos.router)
app.include_router(motoristas.router)
app.include_router(rotas_internas.router)
app.include_router(administradores.router)
app.include_router(horarios_fixos_cliente.router)
app.include_router(reservas.router)

@app.get("/")
def root():
    return {"message": "API para BondRota - Bem-vindo!"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

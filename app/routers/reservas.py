from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import models, schemas

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

# MÉTODO POST... 
# Criando uma nova reserva em um cliente já existente
@router.post("/", response_model=schemas.ReservaResponse, status_code=status.HTTP_201_CREATED)
def criar_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == reserva.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    nova_reserva = models.Reserva(**reserva.dict())
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)
    return nova_reserva

# MÉTODO READ...
# Listar todas as reservas
@router.get("/", response_model=List[schemas.ReservaResponse])
def read_reservas(db: Session = Depends(get_db)):
    reservas = db.query(models.Reserva).all()
    return reservas

# Método READ...
# Listar reservas de um cliente específico
@router.get("/cliente/{cliente_id}", response_model=List[schemas.ReservaResponse])
def read_reservas_cliente_by_id(cliente_id: int, db: Session = Depends(get_db)):
    reservas = db.query(models.Reserva).filter(models.Reserva.id_cliente == cliente_id).all()
    return reservas

# MÉTODO UPDATE...
# Atualiza as reservas de um cliente em específico
@router.patch("/{reserva_id}", response_model=schemas.ReservaResponse)
def atualizar_reserva(reserva_id: int, reserva_update: schemas.ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    # Atualiza apenas os campos enviados (ex: só o status)
    dados_atualizacao = reserva_update.dict(exclude_unset=True)
    
    for key, value in dados_atualizacao.items():
        setattr(db_reserva, key, value)

    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

# MÉTODO DELETE...
# Deletar/Cancelar uma reserva
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_reserva(id: int, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    db.delete(reserva)
    db.commit()
    return None
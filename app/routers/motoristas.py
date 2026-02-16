from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import models, schemas
from algoritmos.criptografia import gerar_hash

router = APIRouter(
    prefix="/motoristas",
    tags=["Motoristas"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MotoristaResponse)
def create_motorista(motorista: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    try:
        dados_motorista = motorista.dict()
        
        dados_motorista['senha'] = gerar_hash(dados_motorista['senha'])

        new_motorista = models.Motorista(**dados_motorista)
        db.add(new_motorista)
        db.commit()
        db.refresh(new_motorista)
        return new_motorista
    except ValueError as e:
        # Captura o erro "Data de Nascimento não pode ser superior..."
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.MotoristaResponse])
def read_motoristas(db: Session = Depends(get_db)):
    motoristas = db.query(models.Motorista).all()
    return motoristas

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.MotoristaResponse)
def read_motoristas_by_id(id: int, db: Session = Depends(get_db)):
    motorista = db.query(models.Motorista).filter(models.Motorista.id == id).first()
    if not motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")
    return motorista

# MÉTODO UPDATE...
@router.put("/{id}", response_model=schemas.MotoristaResponse)
def update_motorista(id: int, motorista_update: schemas.MotoristaCreate, db: Session = Depends(get_db)):
    db_motorista = db.query(models.Motorista).filter(models.Motorista.id == id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    for key, value in motorista_update.dict().items():
        setattr(db_motorista, key, value)
    
    db.commit()
    db.refresh(db_motorista)
    return db_motorista

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_motorista(id: int, db: Session = Depends(get_db)):
    db_motorista = db.query(models.Motorista).filter(models.Motorista.id == id).first()
    if not db_motorista:
        raise HTTPException(status_code=404, detail="Motorista não encontrado")

    db.delete(db_motorista)
    db.commit()
    return None

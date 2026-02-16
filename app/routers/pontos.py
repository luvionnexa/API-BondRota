from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import models, schemas

router = APIRouter(
    prefix="/pontos",
    tags=["Pontos"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PontoResponse)
def create_ponto(ponto: schemas.PontoCreate, db: Session = Depends(get_db)):
    new_ponto = models.Ponto(**ponto.dict())
    db.add(new_ponto)
    db.commit()
    db.refresh(new_ponto)
    return new_ponto

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.PontoResponse])
def read_pontos(db: Session = Depends(get_db)):
    pontos = db.query(models.Ponto).all()
    return pontos

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.PontoResponse)
def read_pontos_by_id(id: int, db: Session = Depends(get_db)):
    ponto = db.query(models.Ponto).filter(models.Ponto.id == id).first()
    if not ponto:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")
    return ponto

# MÉTODO UPDATE...
@router.put("/{id}", response_model=schemas.PontoResponse)
def update_ponto(id: int, ponto_update: schemas.PontoCreate, db: Session = Depends(get_db)):
    db_ponto = db.query(models.Ponto).filter(models.Ponto.id == id).first()
    if not db_ponto:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    for key, value in ponto_update.dict().items():
        setattr(db_ponto, key, value)
    
    db.commit()
    db.refresh(db_ponto)
    return db_ponto

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ponto(id: int, db: Session = Depends(get_db)):
    db_ponto = db.query(models.Ponto).filter(models.Ponto.id == id).first()
    if not db_ponto:
        raise HTTPException(status_code=404, detail="Ponto não encontrado")

    db.delete(db_ponto)
    db.commit()
    return None

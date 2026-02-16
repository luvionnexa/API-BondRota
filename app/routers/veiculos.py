from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import models, schemas

router = APIRouter(
    prefix="/veiculos",
    tags=["Veiculos"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VeiculoResponse)
def create_veiculo(veiculo: schemas.VeiculoCreate, db: Session = Depends(get_db)):
    new_veiculo = models.Veiculo(**veiculo.dict())
    db.add(new_veiculo)
    db.commit()
    db.refresh(new_veiculo)
    return new_veiculo

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.VeiculoResponse])
def read_veiculos(db: Session = Depends(get_db)):
    veiculos = db.query(models.Veiculo).all()
    return veiculos

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.VeiculoResponse)
def read_veiculos_by_id(id: int, db: Session = Depends(get_db)):
    veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")
    return veiculo

# MÉTODO UPDATE...
@router.put("/{id}", response_model=schemas.VeiculoResponse)
def update_veiculo(id: int, veiculo_update: schemas.VeiculoCreate, db: Session = Depends(get_db)):
    db_veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == id).first()
    if not db_veiculo:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")

    for key, value in veiculo_update.dict().items():
        setattr(db_veiculo, key, value)
    
    db.commit()
    db.refresh(db_veiculo)
    return db_veiculo

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_veiculo(id: int, db: Session = Depends(get_db)):
    db_veiculo = db.query(models.Veiculo).filter(models.Veiculo.id == id).first()
    if not db_veiculo:
        raise HTTPException(status_code=404, detail="Veiculo não encontrado")

    db.delete(db_veiculo)
    db.commit()
    return None

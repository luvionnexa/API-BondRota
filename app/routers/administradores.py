from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas
from algoritmos.criptografia import gerar_hash

router = APIRouter(
    prefix="/administradores",
    tags=["Administradores"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdministradorResponse)
def create_administrador(administrador: schemas.AdministradorCreate, db: Session = Depends(get_db)):
    dados_administrador = administrador.dict()
    
    dados_administrador['senha'] = gerar_hash(dados_administrador['senha'])

    new_administrador = models.Administrador(**dados_administrador)
    
    db.add(new_administrador)
    db.commit()
    db.refresh(new_administrador)
    return new_administrador

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.AdministradorResponse])
def read_administradores(db: Session = Depends(get_db)):
    administradores = db.query(models.Administrador).all()
    return administradores

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.AdministradorResponse)
def read_administradores_by_id(id: int, db: Session = Depends(get_db)):
    administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if not administrador:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")
    return administrador

# MÉTODO UPDATE...
@router.put("/{id}", response_model=schemas.AdministradorResponse)
def update_administrador(id: int, administrador_update: schemas.AdministradorCreate, db: Session = Depends(get_db)):
    db_administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if not db_administrador:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    for key, value in administrador_update.dict().items():
        setattr(db_administrador, key, value)
    
    db.commit()
    db.refresh(db_administrador)
    return db_administrador

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_administrador(id: int, db: Session = Depends(get_db)):
    db_administrador = db.query(models.Administrador).filter(models.Administrador.id == id).first()
    if not db_administrador:
        raise HTTPException(status_code=404, detail="Administrador não encontrado")

    db.delete(db_administrador)
    db.commit()
    return None

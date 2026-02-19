from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/rotas_internas",
    tags=["Rotas Internas"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Rotas_InternasResponse)
def create_rotas_internas(rotas_internas: schemas.Rotas_InternasCreate, db: Session = Depends(get_db)):
    new_rotas_internas = models.Rotas_Internas(**rotas_internas.dict())
    db.add(new_rotas_internas)
    db.commit()
    db.refresh(new_rotas_internas)
    return new_rotas_internas

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.Rotas_InternasResponse])
def read_rotas_internas(db: Session = Depends(get_db)):
    rotas_internas = db.query(models.Rotas_Internas).all()
    return rotas_internas

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.Rotas_InternasResponse)
def read_rotas_internas_by_id(id: int, db: Session = Depends(get_db)):
    rotas_interna = db.query(models.Rotas_Internas).filter(models.Rotas_Internas.id == id).first()
    if not rotas_interna:
        raise HTTPException(status_code=404, detail="Rotas_Internas não encontrado")
    return rotas_interna

# MÉTODO UPDATE...
@router.put("/{id}", response_model=schemas.Rotas_InternasResponse)
def update_rotas_interna(id: int, rotas_interna_update: schemas.Rotas_InternasCreate, db: Session = Depends(get_db)):
    db_rotas_interna = db.query(models.Rotas_Internas).filter(models.Rotas_Internas.id == id).first()
    if not db_rotas_interna:
        raise HTTPException(status_code=404, detail="Rotas_Internas não encontrado")

    for key, value in rotas_interna_update.dict().items():
        setattr(db_rotas_interna, key, value)
    
    db.commit()
    db.refresh(db_rotas_interna)
    return db_rotas_interna

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rotas_interna(id: int, db: Session = Depends(get_db)):
    db_rotas_interna = db.query(models.Rotas_Internas).filter(models.Rotas_Internas.id == id).first()
    if not db_rotas_interna:
        raise HTTPException(status_code=404, detail="Rotas_Internas não encontrado")

    db.delete(db_rotas_interna)
    db.commit()
    return None

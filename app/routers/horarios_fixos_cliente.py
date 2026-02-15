# app/routers/horarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/horarios-fixos",
    tags=["Horários Fixos"]
)

# MÉTODO CREATE...
# Criar novo horário fixo de um aluno
@router.post("/", response_model=schemas.HorarioFixoClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_horario(horario: schemas.HorarioFixoClienteCreate, db: Session = Depends(get_db)):
    # Verifica se o cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == horario.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Verifica duplicidade (mesmo cliente, mesmo dia)
    existente = db.query(models.HorarioFixoCliente).filter(
        models.HorarioFixoCliente.id_cliente == horario.id_cliente,
        models.HorarioFixoCliente.dia_semana == horario.dia_semana
    ).first()
    
    if existente:
        raise HTTPException(status_code=400, detail="Este horário já existe para este cliente.")

    novo_horario = models.HorarioFixoCliente(**horario.dict())
    db.add(novo_horario)
    db.commit()
    db.refresh(novo_horario)
    return novo_horario

# MÉTODO READ ...
# Listar TODOS 
@router.get("/", response_model=List[schemas.HorarioFixoClienteResponse])
def listar_todos_horarios(db: Session = Depends(get_db)):
    return db.query(models.HorarioFixoCliente).all()

# MÉTODO READ ...
# Listar horários de UM cliente
@router.get("/cliente/{cliente_id}", response_model=List[schemas.HorarioFixoClienteResponse])
def listar_horarios_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return db.query(models.HorarioFixoCliente).filter(models.HorarioFixoCliente.id_cliente == cliente_id).all()

# MÉTODO UPDATE...
# 4. Atualizar (Ex: Aluno quer trocar de Segunda(2) para Terça(3))
@router.patch("/{id}", response_model=schemas.HorarioFixoClienteResponse)
def atualizar_horario(id: int, horario_update: schemas.HorarioFixoClienteUpdate, db: Session = Depends(get_db)):
    db_horario = db.query(models.HorarioFixoCliente).filter(models.HorarioFixoCliente.id == id).first()

    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")

    # Verifica se a troca causaria duplicidade (ex: já tem Terça cadastrada)
    if horario_update.dia_semana:
        duplicado = db.query(models.HorarioFixoCliente).filter(
            models.HorarioFixoCliente.id_cliente == db_horario.id_cliente, # mesmo dono
            models.HorarioFixoCliente.dia_semana == horario_update.dia_semana # novo dia
        ).first()
        if duplicado and duplicado.id != id:
             raise HTTPException(status_code=400, detail="O cliente já possui este dia fixo cadastrado.")

    # Atualiza
    dados = horario_update.dict(exclude_unset=True)
    for key, value in dados.items():
        setattr(db_horario, key, value)

    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

# MÉTODO DELETE...
# Deletar um horário específico
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_horario(id: int, db: Session = Depends(get_db)):
    horario = db.query(models.HorarioFixoCliente).filter(models.HorarioFixoCliente.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    
    db.delete(horario)
    db.commit()
    return None
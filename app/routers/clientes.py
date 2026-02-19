from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from app.database import get_db
from app import models, schemas
from app.algoritmos.criptografia import gerar_hash
from app.algoritmos.relogio import TimeService

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

# MÉTODO POST...
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ClienteResponse)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    try:
        # 1. Separar os dados do Cliente dos dados das listas
        dados_cliente = cliente.dict()
        # Removemos as listas do dicionário principal para não dar erro ao criar o objeto Cliente
        dias_selecionados = dados_cliente.pop("dias_semana", [])

        # 2. Criptografia da senha (lembra da nossa conversa anterior?)
        dados_cliente['senha'] = gerar_hash(dados_cliente['senha'])

        # 3. Cria o objeto Cliente
        novo_cliente = models.Cliente(**dados_cliente)
        
        # 4. Preencher os horarios e reservas do cliente automaticamente
        # --- LÓGICA DE TEMPO USANDO O SEU TIME SERVICE ---
        # Obtém a data oficial via NTP (ou cache/fallback local)
        hoje = TimeService.obter_data_valida() 
        
        # Encontra a segunda-feira da semana atual
        # weekday() no Python: 0=Segunda, 6=Domingo
        segunda_feira = hoje - timedelta(days=hoje.weekday())

        for dia in dias_selecionados:
            # [cite_start]A. Preenche a tabela 'horario_fixo_cliente' [cite: 8]
            novo_horario = models.HorarioFixoCliente(dia_semana=dia)
            novo_cliente.horarios.append(novo_horario)

            # [cite_start]B. Preenche a tabela 'reservas' para a semana atual [cite: 9]
            # No seu SQL dia 1=Segunda, então subtraímos 1 para o timedelta
            data_calculada = segunda_feira + timedelta(days=(dia - 1))
            
            # Só cria reserva para dias que ainda não passaram nesta semana
            if data_calculada >= hoje:
                nova_reserva = models.Reserva(
                    data_reserva=data_calculada,
                    status='confirmado'
                )
                novo_cliente.reservas.append(nova_reserva)

        # 5. Salva TUDO de uma vez
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        
        return novo_cliente

    except ValueError as e:
        # Captura o erro "Data de Nascimento não pode ser superior..."
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
    """
    new_cliente = models.Cliente(**cliente.dict())
    db.add(new_cliente)
    db.commit()
    db.refresh(new_cliente)
    return new_cliente"""

# MÉTODO READ (todos)...
@router.get("/", response_model=List[schemas.ClienteResponse])
def read_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes

# MÉTODO READ (individual)...
@router.get("/{id}", response_model=schemas.ClienteResponse)
def read_clientes_by_id(id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

# MÉTODO UPDATE...
@router.patch("/{id}", response_model=schemas.ClienteResponse)
def update_cliente(id: int, cliente_update: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    for key, value in cliente_update.dict().items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# MÉTODO DELETE...
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    db.delete(db_cliente)
    db.commit()
    return None

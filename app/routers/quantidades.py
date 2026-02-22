"""
Arquivo com as routes de quantidades
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from algoritmos.relogio import TimeService

router = APIRouter(
    prefix="/quantidades",
    tags=["Quantidades"]
)

# MÉTODO GET (quantidade total, e clientes, que vão para um ponto em específico)
@router.get("/{id_ponto}", status_code=status.HTTP_200_OK)
def read_clientes_in_pontos_by_id(id_ponto: int, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    try:

        query = db.query(models.Cliente).filter(models.Cliente.id_ponto == id_ponto)
        total = query.count()
        clientes = query.offset(skip).limit(limit).all()

        #Separação usando paginação
        return {
            "total": total,
            "page_size": len(clientes),
            "data": clientes 
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


# MÉTODO GET (quantidade diaria de alunos que vão hoje)
"""
Verifica o dia de hj e se existem reservas com esse mesmo dia.
"""
@router.get("/", status_code=status.HTTP_200_OK)
def quantidade_diaria_hoje(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    try:
        #Variáveis e acesso
        hoje = TimeService.obter_data_valida()
        query = db.query(models.Reserva).filter(models.Reserva.data_reserva == hoje)
        total = query.count()
        clientes = query.offset(skip).limit(limit).all()

        #Separação por paginação
        return {
            "total": total,
            "page-size": len(clientes),
            "data": clientes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


"""
Sugestão de IA:

import logging
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

# Configuração básica de log (idealmente configurado no início do app)
logger = logging.getLogger(__name__)

@router.get("/", status_code=status.HTTP_200_OK)
def quantidade_diaria_hoje(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    try:
        hoje = TimeService.obter_data_valida()
        query = db.query(models.Reserva).filter(models.Reserva.data_reserva == hoje)
        
        total = query.count()
        clientes = query.offset(skip).limit(limit).all()

        return {
            "total": total,
            "page-size": len(clientes),
            "data": clientes
        }

    # 1. Erros específicos do Banco de Dados
    except SQLAlchemyError as e:
        # Logamos o erro técnico para o desenvolvedor ver no terminal/arquivo
        logger.error(f"Erro de banco de dados na rota quantidade_diaria: {str(e)}")
        
        # Retornamos uma mensagem limpa para o cliente
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de banco de dados temporariamente indisponível."
        )

    # 2. Erros de lógica de negócio (ex: o TimeService falhou)
    except ValueError as e:
        # Se o TimeService lançar um ValueError, capturamos aqui
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro ao processar data: {str(e)}"
        )

    # 3. "Catch-all" para qualquer outra coisa (Ouro de Segurança)
    except Exception as e:
        # Log detalhado com stack trace para debug imediato
        logger.exception("Erro não esperado na rota quantidade_diaria")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno ao processar a contagem diária."
        )
"""
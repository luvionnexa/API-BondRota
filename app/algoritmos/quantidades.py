"""
Arquivo com as funções de quantidades
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
#####@router.get("/", status_code=status.HTTP_200_OK)
#####def :

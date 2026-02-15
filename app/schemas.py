from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# --- Schemas Ponto ---
class PontoBase(BaseModel):
    nome: str
    rua: str
    cidade: str
    latitude: float
    longitude: float

class PontoCreate(PontoBase):
    pass

class PontoUpdate(BaseModel):
    nome: Optional[str] = None
    rua: Optional[str] = None
    cidade: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PontoResponse(PontoBase):
    id: int
    class Config:
        from_attributes = True


# --- Schemas Rotas Internas ---
class Rotas_InternasBase(BaseModel):
    locais: List[str]
    cidade: str

class Rotas_InternasCreate(Rotas_InternasBase):
    pass

class Rotas_InternasUpdate(BaseModel):
    locais: Optional[List[str]] = None
    cidade: Optional[str] = None

class Rotas_InternasResponse(Rotas_InternasBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas Horarios Fixos ---
class HorarioFixoClienteBase(BaseModel):
    id_cliente: int
    dia_semana: int

class HorarioFixoClienteCreate(HorarioFixoClienteBase):
    pass

class HorarioFixoClienteUpdate(BaseModel):
    dia_semana: Optional[int] = None

class HorarioFixoClienteResponse(HorarioFixoClienteBase):
    id: int
    class Config:
        from_attributes = True

    #Schema Nested
class HorarioFixoClienteCreateNested(BaseModel):
    dia_semana: int

# --- Schemas Reservas ---
class ReservaBase(BaseModel):
    id_cliente: int
    data_reserva: date
    status: Optional[str] = "confirmado"

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    status: Optional[str] = None

class ReservaResponse(ReservaBase):
    id: int
    class Config:
        from_attributes = True

    #Schema Nested
class ReservaCreateNested(BaseModel):
    data_reserva: date
    status: str = "confirmado"


# --- Schemas Clientes ---
class ClienteBase(BaseModel):
    nome: str
    curso: Optional[str] = "nenhum"
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    senha: str
    turno: str
    foto: Optional[str] = None
    conta: str
    # Opcionais pois podem ser nulos no banco (ON DELETE SET NULL)
    id_rota_interna: Optional[int] = None
    id_ponto: Optional[int] = None
    faltas: Optional[int] = None
    dias_semana: List[int] = []

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    curso: Optional[str] = None
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    senha: Optional[str] = None
    turno: Optional[str] = None
    foto: Optional[str] = None
    conta: Optional[str] = None
    id_rota_interna: Optional[int] = None
    id_ponto: Optional[int] = None
    faltas: Optional[int] = None

class ClienteResponse(ClienteBase):
    id: int
    # Para não retornar a senha no response, é boa prática excluí-la ou criar um schema específico
    class Config:
        from_attributes = True

# --- Schemas Motorista ---
class MotoristaBase(BaseModel):
    nome: str
    senha: str
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    turno: str
    foto: Optional[str] = None
    cidade_de_trabalho: str
    residencia: str
    qtd_viagens: int

class MotoristaCreate(MotoristaBase):
    pass

class MotoristaUpdate(BaseModel):
    nome: Optional[str] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None
    data_de_nascimento: Optional[date] = None
    turno: Optional[str] = None
    foto: Optional[str] = None
    cidade_de_trabalho: Optional[str] = None
    residencia: Optional[str] = None
    qtd_viagens: Optional[int] = None

class MotoristaResponse(MotoristaBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas Veiculo ---
class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    capacidade: int
    estancia: str
    status: bool
    usos_dia: Optional[int] = 0
    ar_condicionado: bool
    banheiro: bool
    persiana: bool
    luz_de_leitura: bool
    tomada: bool

class VeiculoCreate(VeiculoBase):
    pass

class VeiculoUpdate(BaseModel):
    placa: Optional[str] = None
    modelo: Optional[str] = None
    capacidade: Optional[int] = None
    estancia: Optional[str] = None
    status: Optional[bool] = None
    usos_dia: Optional[int] = None
    ar_condicionado: Optional[bool] = None
    banheiro: Optional[bool] = None
    persiana: Optional[bool] = None
    luz_de_leitura: Optional[bool] = None
    tomada: Optional[bool] = None

class VeiculoResponse(VeiculoBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas Administrador ---
class AdministradorBase(BaseModel):
    email: str
    senha: str
    cidade: str

class AdministradorCreate(AdministradorBase):
    pass

class AdministradorResponse(BaseModel):
    id: int
    email: str
    cidade: str
    class Config:
        from_attributes = True


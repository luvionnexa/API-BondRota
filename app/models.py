from sqlalchemy import Column, Integer, String, VARCHAR, Boolean, ForeignKey, Date, CheckConstraint, Numeric
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, validates
from app.database import Base # Certifique-se que o import do Base está correto no seu projeto
from algoritmos.time import validar_data_nao_futura

# ---Modelo das tabelas---

class Ponto(Base):
    __tablename__ = "pontos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    rua = Column(VARCHAR(255), nullable=False)
    cidade = Column(VARCHAR(100), nullable=False)
    latitude = Column(Numeric(9,6), nullable=False)
    longitude = Column(Numeric(9,6), nullable=False)

    clientes = relationship("Cliente", back_populates="ponto")

class Rotas_Internas(Base):
    __tablename__ = "rotas_internas"
    
    id = Column(Integer, primary_key=True, index=True)
    cidade = Column(VARCHAR(100), nullable=False)
    locais = Column(ARRAY(VARCHAR(255)), nullable=False)

    clientes = relationship("Cliente", back_populates="rota_interna")

class Motorista(Base):
    __tablename__ = "motoristas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    senha = Column(VARCHAR(255), nullable=False)
    telefone = Column(VARCHAR(15))
    data_de_nascimento = Column(Date)
    turno = Column(VARCHAR(2), CheckConstraint("turno IN ('MT', 'VT', 'NT')"), nullable=False)
    foto = Column(VARCHAR(2048))
    cidade_de_trabalho = Column(VARCHAR(100), nullable=False)
    residencia = Column(VARCHAR(100), nullable=False)
    qtd_viagens = Column(Integer, CheckConstraint('qtd_viagens >= 0'))

    @validates('data_de_nascimento')
    def validate_nascimento(self, key, value):
        # Chama a função utilitária passando o valor e o nome para o erro
        return validar_data_nao_futura(value, "Data de Nascimento")

class Veiculo(Base):
    __tablename__ = "veiculos"
    
    id = Column(Integer, primary_key=True, index=True)
    placa = Column(VARCHAR(7), nullable=False)
    modelo = Column(VARCHAR(30), nullable=False)
    capacidade = Column(Integer, CheckConstraint('capacidade > 0'), nullable=False)
    estancia = Column(VARCHAR(100), nullable=False)
    status = Column(Boolean, nullable=False)
    usos_dia = Column(Integer)
    ar_condicionado = Column(Boolean, nullable=False)
    banheiro = Column(Boolean, nullable=False)
    persiana = Column(Boolean, nullable=False)
    luz_de_leitura = Column(Boolean, nullable=False)
    tomada = Column(Boolean, nullable=False)

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(VARCHAR(100), nullable=False)
    curso = Column(VARCHAR(50), default='nenhum')
    telefone = Column(VARCHAR(15))
    data_de_nascimento = Column(Date)
    senha = Column(VARCHAR(255), nullable=False)
    turno = Column(VARCHAR(2), CheckConstraint("turno IN ('MT', 'VT', 'NT', 'IN')"), nullable=False)
    foto = Column(VARCHAR(2048))
    conta = Column(VARCHAR(20), CheckConstraint("conta IN ('estudante', 'estagio')"), nullable=False)
    faltas = Column(Integer, CheckConstraint('faltas >= 0'), default= 0)

    # Foreign Keys (usando strings para evitar erro de ordem de leitura)
    # Definidas como nullable=True para suportar ON DELETE SET NULL
    id_rota_interna = Column(Integer, ForeignKey("rotas_internas.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    id_ponto = Column(Integer, ForeignKey("pontos.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    # Relacionamentos
    rota_interna = relationship("Rotas_Internas", back_populates="clientes")
    ponto = relationship("Ponto", back_populates="clientes")
    
    # Novos relacionamentos
    horarios = relationship("HorarioFixoCliente", back_populates="cliente", cascade="all, delete")
    reservas = relationship("Reserva", back_populates="cliente", cascade="all, delete")

    @validates('data_de_nascimento')
    def validate_nascimento(self, key, value):
        # Chama a função utilitária passando o valor e o nome para o erro
        return validar_data_nao_futura(value, "Data de Nascimento")

class Administrador(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR(100), nullable=False)
    senha = Column(VARCHAR(255), nullable=False)
    cidade = Column(VARCHAR(100), nullable=False)

class HorarioFixoCliente(Base):
    __tablename__ = "horarios_fixos_cliente"
    
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(Integer, CheckConstraint("dia_semana BETWEEN 1 AND 5"), nullable=False)

    cliente = relationship("Cliente", back_populates="horarios")

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)
    data_reserva = Column(Date, nullable=False)
    status = Column(String, CheckConstraint("status IN ('confirmado', 'cancelado')"), default='confirmado', nullable=False)

    cliente = relationship("Cliente", back_populates="reservas")
from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Optional

from model import BaseModel

class ProdutoModel(BaseModel):
    __tablename__ = "produtos"

    id = Column("produto_id", Integer, primary_key=True)
    nome = Column(String(250), unique=True)
    estoque = Column(Integer)
    preco_unitario = Column(Float)
    data_criacao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, estoque: int, preco_unitario: float, data_criacao: Optional[DateTime] = None):
        self.nome = nome
        self.estoque = estoque
        self.preco_unitario = preco_unitario
        if data_criacao:
            self.data_criacao = data_criacao

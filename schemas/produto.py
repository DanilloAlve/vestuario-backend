from pydantic import BaseModel
from typing import List, Optional

class ProdutoSchema(BaseModel):
    nome: str
    estoque: int
    preco_unitario: float

class ProdutoViewSchema(BaseModel):
    id: int
    nome: str
    estoque: int
    preco_unitario: float

class ListagemProdutosSchema(BaseModel):
    lista_produtos: List[ProdutoViewSchema]

class ProdutoBuscaSchema(BaseModel):
    nome: str

class ProdutoRemoverSchema(BaseModel):
    mensagem: str
    nome: str

class ProdutoAtualizarSchema(BaseModel):
    nome: str
    estoque: Optional[int]

def exibir_produto(produto):
    return {
        "id": produto.id,
        "nome": produto.nome,
        "estoque": produto.estoque,
        "preco_unitario": produto.preco_unitario
    }

def exibir_produtos(produtos):
    resultado = []
    for item in produtos:
        resultado.append({
            "id": item.id,
            "nome": item.nome,
            "estoque": item.estoque,
            "preco_unitario": item.preco_unitario
        })
    return {"lista_produtos": resultado}

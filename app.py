from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import DBSession, produto
from logger import logger
from schemas import *
from flask_cors import CORS



info = Info(title="Sistema de Gerenciamento de Produtos", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Escolha entre Swagger, ReDoc ou RapiDoc.")
produto_tag = Tag(name="Produto", description="Operações relacionadas ao gerenciamento de produtos.")


@app.get('/', tags=[home_tag])
def pagina_inicial():
    """Redireciona para a documentação no caminho /openapi."""
    return redirect('/openapi')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErroSchema, "400": ErroSchema})
def criar_produto(formulario: ProdutoSchema):
    """Cria um novo produto no banco de dados.

    Retorna o produto criado.
    """
    novo_produto = Produto(
        nome=formulario.nome,
        quantidade=formulario.quantidade,
        valor_unitario=formulario.valor_unitario)
    logger.debug(f"Registrando novo produto: '{novo_produto.nome}'")
    try:
        conexao = Session()
        conexao.add(novo_produto)
        conexao.commit()
        logger.debug(f"Produto '{novo_produto.nome}' registrado com sucesso")
        return apresenta_produto(novo_produto), 200
    
    except IntegrityError:
        mensagem_erro = "Já existe um produto com esse nome no banco de dados."
        logger.warning(f"Falha ao registrar produto '{novo_produto.nome}': {mensagem_erro}")
        return {"message": mensagem_erro}, 409
    
    except Exception:
        mensagem_erro = "Ocorreu um erro inesperado ao tentar cadastrar o produto."
        logger.error(f"Erro ao registrar produto '{novo_produto.nome}': {mensagem_erro}")
        return {"message": mensagem_erro}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErroSchema})
def listar_produtos():
    """Obtém a lista de produtos cadastrados.

    Retorna uma lista de produtos.
    """
    logger.debug(f"Buscando todos os produtos cadastrados...")
    conexao = Session()
    lista_produtos = conexao.query(Produto).all()

    if not lista_produtos:
        return {"produtos": []}, 200
    else:
        logger.debug(f"{len(lista_produtos)} produtos encontrados.")
        return apresenta_produtos(lista_produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErroSchema})
def buscar_produto(query: ProdutoBuscaSchema):
    """Busca um produto específico pelo nome.

    Retorna os detalhes do produto encontrado.
    """
    nome_produto = query.nome
    logger.debug(f"Buscando informações do produto '{nome_produto}'...")
    conexao = Session()
    produto_encontrado = conexao.query(Produto).filter(Produto.nome == nome_produto).first()

    if not produto_encontrado:
        mensagem_erro = "Produto não encontrado."
        logger.warning(f"Falha ao encontrar o produto '{nome_produto}': {mensagem_erro}")
        return {"message": mensagem_erro}, 404
    else:
        logger.debug(f"Produto '{nome_produto}' encontrado.")
        return apresenta_produto(produto_encontrado), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoSchema, "404": ErroSchema})
def remover_produto(query: ProdutoBuscaSchema):
    """Remove um produto pelo nome informado.

    Retorna uma mensagem de confirmação da remoção.
    """
    nome_produto = unquote(unquote(query.nome))
    logger.debug(f"Removendo o produto '{nome_produto}'...")
    conexao = Session()
    deletados = conexao.query(Produto).filter(Produto.nome == nome_produto).delete()
    conexao.commit()

    if deletados:
        logger.debug(f"Produto '{nome_produto}' removido com sucesso.")
        return {"message": "Produto removido", "nome": nome_produto}, 200
    else:
        mensagem_erro = "Produto não encontrado."
        logger.warning(f"Falha ao remover o produto '{nome_produto}': {mensagem_erro}")
        return {"message": mensagem_erro}, 404


@app.put('/editar_produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "409": ErroSchema, "400": ErroSchema})
def atualizar_produto(formulario: ListagemProdutosSchema):
    """Atualiza as informações de um produto existente.

    Retorna o produto atualizado.
    """
    nome_produto = formulario.nome
    conexao = Session()

    try:
        query = conexao.query(Produto).filter(Produto.nome == nome_produto)
        produto_existente = query.first()

        if not produto_existente:
            mensagem_erro = "Produto não encontrado."
            logger.warning(f"Falha ao encontrar o produto '{nome_produto}': {mensagem_erro}")
            return {"message": mensagem_erro}, 404
        else:
            if formulario.quantidade:
                produto_existente.quantidade = formulario.quantidade
            
            conexao.add(produto_existente)
            conexao.commit()
            logger.debug(f"Produto '{produto_existente.nome}' atualizado com sucesso.")
            return apresenta_produto(produto_existente), 200
    except Exception:
        mensagem_erro = "Erro ao atualizar o produto."
        logger.error(f"Erro ao atualizar produto '{produto_existente.nome}': {mensagem_erro}")
        return {"message": mensagem_erro}, 400

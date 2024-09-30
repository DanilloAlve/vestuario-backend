from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from model.base import BaseModel
from model.produto import ProdutoModel

db_directory = "db_data/"
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

db_connection = f"sqlite:///{db_directory}/database.sqlite3"

# Criação da engine de conexão com o banco de dados
engine = create_engine(db_connection, echo=False)

# Criação da sessão de banco de dados
DBSession = sessionmaker(bind=engine)

# Verificação se o banco existe e criação se necessário
if not database_exists(engine.url):
    create_database(engine.url)

# Criação das tabelas no banco de dados
BaseModel.metadata.create_all(engine)

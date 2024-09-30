# vestuario-backend

Este projeto em requisito para Pós-Graduação em Desenvolvimento FullStack PUC-RIO e consiste em uma API Flask para gerenciamento de produtos de vestuário. A API permite realizar operações CRUD (Create, Read, Update, Delete) sobre produtos. Abaixo estão as instruções para configurar e executar o ambiente localmente. 

https://drive.google.com/file/d/17J9kJ9PPd8HxOPKvYv8tCpLyIfADy-M3/view?usp=sharing

## Passo a passo para execução

### 1. Clone o repositório

git clone https://github.com/seu-usuario/dani-modas-backend.git

### 2. Crie um ambiente virtual 
Se você quiser isolar as dependências do projeto, use o virtualenv para criar um ambiente virtual:

python -m venv venv

### 3. Ative o ambiente virtual

venv\Scripts\activate

### 4. Instale as dependências
Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo requirements.txt:

pip install -r requirements.txt

### 5. Execute a aplicação
Agora que tudo está configurado, você pode executar o backend usando o comando:

flask run --host=0.0.0.0 --port=5000
A API estará disponível no endereço:

http://localhost:5000

### 6. Acesse a documentação da API
A API utiliza Swagger para documentar todas as rotas disponíveis. A documentação pode ser acessada em:

http://localhost:5000/openapi

### Executando com Docker
Para rodar o backend usando Docker, siga os passos abaixo:

### 1. Construir a imagem Docker
Na raiz do projeto, onde o arquivo Dockerfile está localizado, execute o seguinte comando para construir a imagem Docker:

docker build -t dani-modas-backend .

### 2. Executar o container
Após a imagem ser construída, você pode rodar a aplicação em um container Docker com o seguinte comando:

docker run -d -p 5000:5000 dani-modas-backend
http://localhost:5000

### 3. Verificar o status do container
Para garantir que o container está rodando corretamente, você pode listar os containers ativos com:

docker ps

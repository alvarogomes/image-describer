# Image-Describer

## Descrição

O projeto "Image-Describer" é uma API FastAPI que aceita uma imagem e um prompt como entrada. Utilizando um modelo de Inteligência Artificial, a API gera uma descrição textual da imagem e retorna essa descrição juntamente com as entidades detectadas na imagem.

## Pré-requisitos

- Python 3.8 ou superior
- Docker (opcional)

## Instalação

### Instalação Manual

1. Clone o repositório:

   ```
   git clone https://github.com/alvarogomes/image-describer.git
   ```

2. Navegue até o diretório do projeto:

   ```
   cd image-describer
   ```

3. Instale as dependências necessárias:

   ```
   pip install -r requirements.txt
   ```

### Utilizando Docker

Se você preferir usar Docker, o projeto já vem com um `Dockerfile` e um arquivo `docker-compose.yml`.

## Execução

### Execução Manual

1. Execute o seguinte comando para iniciar o servidor FastAPI:

   ```
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   **Nota:** Substitua `main` pelo nome do seu arquivo que contém o app FastAPI.

2. A API deve agora estar rodando em [http://localhost:8000](http://localhost:8000).

### Utilizando Docker-Compose

1. Construa a imagem do Docker:

   ```
   docker-compose build
   ```

2. Inicie o contêiner:

   ```
   docker-compose up
   ```

   A API estará disponível em [http://localhost:8000](http://localhost:8000), e o MinIO estará disponível em [http://localhost:9000](http://localhost:9000).

## Uso da API

Envie uma solicitação POST para `http://localhost:8000/process` com um arquivo de imagem e um prompt como parâmetros do formulário. O sistema retornará uma descrição textual da imagem e as entidades detectadas.

Por exemplo, utilizando `curl`:

```bash
curl -X 'POST' \
  'http://localhost:8000/process' \
  -H 'accept: application/json' \
  -F 'image=@path/to/your/image.jpg' \
  -F 'prompt=Describe the image'
```
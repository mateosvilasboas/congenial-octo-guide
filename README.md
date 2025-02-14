# Projeto Leitura de API 

O objetivo desse projeto é ler e agregar dados de uma API de contas de anúncios de clientes imaginários e formatá-los em .csv. Feito com Python 3.10.12.

## Instalação

Assumindo que você já tenha instalado `Python 3.10.12` ou versão superior em sua máquina, utilizando-se de um terminal:

1. Clone o projeto em uma pasta
2. Crie um virtual enviroment para o projeto python: `python3 -m venv .venv`
3. Instale as dependências do projeto: `pip install -r requirements.txt`

## Inicialização
Para iniciar o servidor em um terminal: `flask --app app --debug run`. O servidor pode ser acessado através de `http://127.0.0.1:5000`.

## Endpoints
A aplicação conta com os seguintes endpoints:

- `GET /geral/`: extrai dados de todas as plataformas de anúncios presentes na API e os salva em .csv (`data.csv`) na raiz do projeto
- `GET /geral/resumo/`: extrai dados de todas as plataformas de anúncios presentes na API, resumindo-os por plataforma e conta de cliente e os salva em .csv (`data.csv`) na raiz do projeto
- `GET /<plataforma>/`: extrai dados da plataforma de anúnico presente na API e referida no endpoint e os salva em .csv (`data.csv`) na raiz do projeto
- `GET /<plataforma/resumo/`: extrai dados da plataforma de anúncios presente na API, resumindo-os por conta de cliente e os salva em .csv (`data.csv`) na raiz do projeto

## Lista de melhorias posteriores
- Evitar a sobrescrição do arquivo `data.csv` anterior pelo mais atual.

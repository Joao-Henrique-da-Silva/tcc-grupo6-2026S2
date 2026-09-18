# Backend - TCC Grupo 6

API REST em Flask para o Sistema de Controle de Estoque de Madeiras.

## Requisitos

- Python 3.13
- pip

## Como rodar localmente

### 1. Criar ambiente virtual

    cd software/backend
    python3.13 -m venv venv
    source venv/bin/activate

### 2. Instalar dependencias

    pip install -r requirements.txt

### 3. Configurar variaveis de ambiente

    cp .env.example .env

### 4. Rodar o servidor

    python app.py

O servidor sobe em http://0.0.0.0:5000.

## Endpoints

### Healthcheck
- GET / - verifica se o servidor esta online

### Leituras
- POST /api/leituras - recebe dados do ESP32 (requer token)
- GET /api/leituras - lista leituras
- GET /api/leituras/ultima - ultima leitura

### Madeiras
- GET /api/madeiras - lista todas
- GET /api/madeiras/<id> - detalhes
- POST /api/madeiras - cadastra nova

### Alertas
- GET /api/alertas - lista alertas
- PUT /api/alertas/<id>/resolver - marca como resolvido

### Estatisticas
- GET /api/estatisticas - totais para o dashboard

## Estrutura do banco

Consulte software/database/schema.sql.

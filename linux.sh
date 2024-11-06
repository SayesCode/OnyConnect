#!/bin/bash

echo "Atualizando sistema e instalando dependências..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv tor

# Criação do ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativando o ambiente virtual
echo "Ativando o ambiente virtual..."
source venv/bin/activate

# Instalando FastAPI e dependências no ambiente virtual
echo "Instalando dependências do Python..."
pip install fastapi jinja2 uvicorn python-multipart

echo "Iniciando..."
python src/OnyConnect/main.py &

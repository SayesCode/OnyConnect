#!/bin/bash

# Verifica a arquitetura do sistema
arch=$(uname -m)

# Função para instalar o apt com o gerenciador de pacotes do sistema
install_apt() {
    echo "apt-get não encontrado. Tentando instalar o apt usando o gerenciador de pacotes do sistema..."

    if command -v yum &> /dev/null; then
        sudo yum install -y apt
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y apt
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y apt
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm apt
    else
        echo "Não foi possível encontrar um gerenciador de pacotes compatível para instalar o apt. Instale-o manualmente."
        exit 1
    fi

    # Atualiza o índice de pacotes após a instalação do apt
    sudo apt-get update -y
}

# Verificação do sistema e instalação dos pacotes necessários
if [[ "$arch" == *'arm'* || "$arch" == *'Android'* ]]; then
   pkg install -y tor
   pkg install -y python3
   pkg update && pkg upgrade -y
else
   if ! command -v apt-get &> /dev/null; then
       install_apt
   fi
   echo "Atualizando sistema e instalando dependências..."
   sudo apt-get update -y
   sudo apt-get install -y python3 python3-pip python3-venv tor
fi

# Criação do ambiente virtual
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativando o ambiente virtual
echo "Ativando o ambiente virtual..."
source venv/bin/activate

# Instalando FastAPI e dependências no ambiente virtual
echo "Instalando dependências do Python..."
pip install fastapi jinja2 uvicorn python-multipart

# Iniciando o script principal
echo "Iniciando..."
python src/onyconnect/main.py &

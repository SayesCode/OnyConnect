@echo off
setlocal

:: Verificar se o Docker está instalado
docker --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker não encontrado. Instalando Docker Desktop...

    :: Verificar se Winget está instalado
    where winget >nul 2>nul
    if %errorlevel% equ 0 (
        echo Winget encontrado. Instalando Docker Desktop com Winget...
        winget install -e --id Docker.DockerDesktop -h
        goto :end
    )

    :: Verificar se Chocolatey está instalado
    where choco >nul 2>nul
    if %errorlevel% equ 0 (
        echo Chocolatey encontrado. Instalando Docker Desktop com Chocolatey...
        choco install docker-desktop -y
        goto :end
    )

    :: Verificar se Scoop está instalado
    where scoop >nul 2>nul
    if %errorlevel% equ 0 (
        echo Scoop encontrado. Instalando Docker Desktop com Scoop...
        scoop install docker
        goto :end
    )

    :: Instalar Chocolatey se nenhum gerenciador foi encontrado
    echo Nenhum gerenciador de pacotes encontrado. Instalando Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    
    :: Instalar Docker Desktop com Chocolatey
    choco install docker-desktop -y
)

:: Tentar rodar o Docker Compose
docker-compose up --build -d
if %errorlevel% neq 0 (
    echo Ocorreu um erro ao executar o comando docker-compose. Verifique se o Docker está instalado corretamente.
    echo Se o problema persistir, baixe e instale o Docker manualmente do site oficial: https://www.docker.com/
    goto :end
)

:end
echo Abra: http://127.0.0.1:8000.

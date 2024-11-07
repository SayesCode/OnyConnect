@echo off
setlocal

:: Check if Docker is installed
docker --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker not found. Installing Docker Desktop...

    :: Check if Winget is installed
    where winget >nul 2>nul
    if %errorlevel% equ 0 (
        echo Winget found. Installing Docker Desktop with Winget...
        winget install -e --id Docker.DockerDesktop -h
        goto :end
    )

    :: Check if Chocolatey is installed
    where choco >nul 2>nul
    if %errorlevel% equ 0 (
        echo Chocolatey found. Installing Docker Desktop with Chocolatey...
        choco install docker-desktop -y
        goto :end
    )

    :: Check if Scoop is installed
    where scoop >nul 2>nul
    if %errorlevel% equ 0 (
        echo Scoop found. Installing Docker Desktop with Scoop...
        scoop install docker
        goto :end
    )

    :: Install Chocolatey if no package manager was found
    echo No package manager found. Installing Chocolatey...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    
    :: Install Docker Desktop with Chocolatey
    choco install docker-desktop -y
)

:: Try to run Docker Compose
docker-compose up --build -d
if %errorlevel% neq 0 (
    echo An error occurred when running the docker-compose command. Check if Docker is installed correctly.
    echo If the problem persists, download and install Docker manually from the official website: https://www.docker.com/
    goto :end
)

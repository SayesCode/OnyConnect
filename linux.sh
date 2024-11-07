#!/bin/bash

# Check system architecture
arch=$(uname -m)

# Function to install apt using the system's package manager
install_apt() {
    echo "apt-get not found. Attempting to install apt using the system's package manager..."

    if command -v yum &> /dev/null; then
        sudo yum install -y apt
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y apt
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y apt
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm apt
    else
        echo "Could not find a compatible package manager to install apt. Install it manually."
        exit 1
    fi

    # Update the package index after installing apt
    sudo apt-get update -y
}

# System check and installation of necessary packages
if [[ "$arch" == *'arm'* || "$arch" == *'Android'* ]]; then
   pkg install -y tor
   pkg install -y python3
   pkg update && pkg upgrade -y
else
   if ! command -v apt-get &> /dev/null; then
       install_apt
   fi
   echo "Updating system and installing dependencies..."
   sudo apt-get update -y
   sudo apt-get install -y python3 python3-pip python3-venv tor
fi

# Create the virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Installing FastAPI and dependencies in the virtual environment
echo "Installing Python dependencies..."
pip install fastapi jinja2 uvicorn python-multipart
clear

# Starting the main script
echo "Starting..."
python src/onyconnect/main.py &

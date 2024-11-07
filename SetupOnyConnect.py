import os
import zipfile
import urllib.request
import subprocess
import time
import sys

# Função para baixar o arquivo ZIP
def download_zip(url, save_path):
    urllib.request.urlretrieve(url, save_path)

# Função para extrair o arquivo ZIP
def extract_zip(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

# Função para verificar se o Python está instalado
def check_python_installed():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Função para instalar o Python
def install_python():
    python_installer_url = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
    installer_path = os.path.join(temp_dir, "python_installer.exe")
    urllib.request.urlretrieve(python_installer_url, installer_path)
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"])

# Caminhos
temp_dir = os.path.join(os.environ['TEMP'])
zip_file = os.path.join(temp_dir, "OnyConnect.zip")
extract_dir = os.path.join(temp_dir, "OnyConnect")

# Baixar o arquivo ZIP
github_url = "https://github.com/SayesCode/OnyConnect/archive/refs/heads/main.zip"
download_zip(github_url, zip_file)

# Extrair o conteúdo do arquivo ZIP
extract_zip(zip_file, extract_dir)

# Aguardar 5 segundos para garantir que a extração foi concluída
time.sleep(5)

# Verificar se o Python está instalado
if not check_python_installed():
    print("Python não encontrado. Instalando...")
    install_python()
    time.sleep(10)  # Aguardar 10 segundos para garantir que a instalação do Python foi concluída

# Definir o caminho do executável do Python
python_exe = "python"

# Navegar até o diretório do projeto extraído
project_folder = None
for root, dirs, files in os.walk(extract_dir):
    if "OnyConnect" in dirs:
        project_folder = os.path.join(root, "OnyConnect")
        break

# Instalar as dependências do requirements.txt
requirements_file = os.path.join(project_folder, "requirements.txt")
if os.path.exists(requirements_file):
    subprocess.run([python_exe, "-m", "pip", "install", "-r", requirements_file])

# Rodar o script Python
main_script = os.path.join(project_folder, "main.py")
if os.path.exists(main_script):
    subprocess.run([python_exe, main_script])


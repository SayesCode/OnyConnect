import os
import zipfile
import urllib.request
import subprocess
import time
import sys

# Function to download the ZIP file
def download_zip(url, save_path):
    urllib.request.urlretrieve(url, save_path)

# Function to extract the ZIP file
def extract_zip(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

# Function to check if Python is installed
def check_python_installed():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install Python
def install_python():
    python_installer_url = "https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe"
    installer_path = os.path.join(temp_dir, "python_installer.exe")
    urllib.request.urlretrieve(python_installer_url, installer_path)
    subprocess.run([installer_path, "/quiet", "InstallAllUsers=1", "PrependPath=1"])

# Paths
temp_dir = os.path.join(os.environ['TEMP'])
zip_file = os.path.join(temp_dir, "OnyConnect.zip")
extract_dir = os.path.join(temp_dir, "OnyConnect")

# Download the ZIP file
github_url = "https://github.com/SayesCode/OnyConnect/archive/refs/heads/main.zip"
download_zip(github_url, zip_file)

# Extract the content of the ZIP file
extract_zip(zip_file, extract_dir)

# Wait 5 seconds to ensure extraction is complete
time.sleep(5)

# Check if Python is installed
if not check_python_installed():
    print("Python not found. Installing...")
    install_python()
    time.sleep(10)  # Wait 10 seconds to ensure Python installation is complete

# Define the path for the Python executable
python_exe = "python"

# Navigate to the extracted project directory
project_folder = None
for root, dirs, files in os.walk(extract_dir):
    if "OnyConnect" in dirs:
        project_folder = os.path.join(root, "OnyConnect")
        break

# Install dependencies from requirements.txt
requirements_file = os.path.join(project_folder, "requirements.txt")
if os.path.exists(requirements_file):
    subprocess.run([python_exe, "-m", "pip", "install", "-r", requirements_file])

# Run the Python script
main_script = os.path.join(project_folder, "main.py")
if os.path.exists(main_script):
    subprocess.run([python_exe, main_script])

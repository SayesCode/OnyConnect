import os
import subprocess
import time
import logging

# Configura o logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_onion_service(port):
    try:
        # Define o diretório de configuração com caminho absoluto
        base_dir = os.path.abspath("src/onyconnect/config")
        service_dir = os.path.join(base_dir, "hidden_service")
        
        # Cria o diretório para o serviço .onion com permissões corretas
        logging.info("Criando diretório para o serviço .onion.")
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)  # Permissões restritas para Tor
        
        # Lê o template do torrc e insere as variáveis necessárias
        logging.info("Lendo e configurando o template torrc.")
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=service_dir)
        
        # Salva o conteúdo no arquivo torrc
        torrc_path = os.path.join(base_dir, "torrc")
        logging.info(f"Salvando configuração torrc em {torrc_path}.")
        with open(torrc_path, "w") as file:
            file.write(torrc_content)

        # Inicia o Tor com o arquivo torrc especificado
        logging.info("Iniciando o processo Tor.")
        tor_process = subprocess.Popen(["tor", "-f", torrc_path])

        # Aguardar para garantir que o Tor tenha tempo para gerar o hostname
        time.sleep(5)

        # Verificar se o arquivo hostname foi criado
        hostname_path = os.path.join(service_dir, "hostname")
        if os.path.exists(hostname_path):
            logging.info("Arquivo hostname encontrado. Lendo hostname.")
            with open(hostname_path, "r") as file:
                hostname = file.read().strip()
            # Finalizar o processo do Tor após gerar o hostname
            logging.info("Hostname gerado com sucesso. Finalizando processo Tor.")
            tor_process.terminate()
            return hostname
        else:
            # Finalizar o processo do Tor em caso de erro
            logging.error("Arquivo hostname não encontrado. Finalizando processo Tor.")
            tor_process.terminate()
            raise FileNotFoundError("Arquivo hostname não encontrado. Verifique as permissões e configuração do Tor.")
    except Exception as e:
        logging.error(f"Erro ao gerar o serviço .onion: {e}")
        return None

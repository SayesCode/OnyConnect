import os
import subprocess
import time

def generate_onion_service(port):
    try:
        # Define o diretório de configuração com caminho absoluto
        base_dir = os.path.abspath("src/onyconnect/config")
        service_dir = os.path.join(base_dir, "hidden_service")
        
        # Cria o diretório para o serviço .onion com permissões corretas
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)  # Permissões restritas para Tor
        
        # Lê o template do torrc e insere as variáveis necessárias
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=service_dir)
        
        # Salva o conteúdo no arquivo torrc
        torrc_path = os.path.join(base_dir, "torrc")
        with open(torrc_path, "w") as file:
            file.write(torrc_content)

        # Inicia o Tor com o arquivo torrc especificado
        tor_process = subprocess.Popen(["tor", "-f", torrc_path])

        # Aguardar para garantir que o Tor tenha tempo para gerar o hostname
        time.sleep(5)

        # Verificar se o arquivo hostname foi criado
        hostname_path = os.path.join(service_dir, "hostname")
        if os.path.exists(hostname_path):
            with open(hostname_path, "r") as file:
                hostname = file.read().strip()
            # Finalizar o processo do Tor após gerar o hostname
            tor_process.terminate()
            return hostname
        else:
            # Finalizar o processo do Tor em caso de erro
            tor_process.terminate()
            raise FileNotFoundError("Arquivo hostname não encontrado. Verifique as permissões e configuração do Tor.")
    except Exception as e:
        print(f"Erro ao gerar o serviço .onion: {e}")
        return None

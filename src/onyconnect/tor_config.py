import os
import subprocess

def generate_onion_service(port):
    try:
        # Definindo o diretório padrão com caminho absoluto
        base_dir = os.path.abspath("src/onyconnect/config")
        service_dir = os.path.join(base_dir, "hidden_service")
        
        # Criando o diretório com as permissões corretas
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)  # Permissões restritas para Tor
        
        # Lendo o template torrc e substituindo a porta
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=service_dir)
        
        # Criando o arquivo torrc
        with open(os.path.join(base_dir, "torrc"), "w") as file:
            file.write(torrc_content)

        # Executando o Tor
        subprocess.run(["tor", "-f", os.path.join(base_dir, "torrc")])

        # Lendo o hostname do serviço .onion gerado
        hostname_path = os.path.join(service_dir, "hostname")
        with open(hostname_path, "r") as file:
            hostname = file.read().strip()
        
        return hostname
    except Exception as e:
        print(f"Erro ao gerar o serviço .onion: {e}")
        return None

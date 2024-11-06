import os
import subprocess

def generate_onion_service(port, directory):
    try:
        # Caminho para o diretório do serviço Onion
        service_dir = "/tmp/hidden_service/"  # Ajustado para diretório temporário
        os.makedirs(service_dir, exist_ok=True)

        # Lendo o template torrc e substituindo as variáveis
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=directory)
        
        # Criando o arquivo torrc
        with open("src/onyconnect/config/torrc", "w") as file:
            file.write(torrc_content)

        # Executando o Tor
        subprocess.run(["tor", "-f", "src/onyconnect/config/torrc"])

        # Lendo o hostname do serviço .onion gerado
        with open(os.path.join(service_dir, "hostname"), "r") as file:
            hostname = file.read().strip()
        
        return hostname
    except Exception as e:
        print(f"Erro ao gerar o serviço .onion: {e}")
        return None

import os
import subprocess

def generate_onion_service(port, directory):
    try:
        service_dir = "/var/lib/tor/hidden_service/"
        os.makedirs(service_dir, exist_ok=True)

        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=directory)
        
        with open("src/onyconnect/config/torrc", "w") as file:
            file.write(torrc_content)

        subprocess.run(["tor", "-f", "src/onyconnect/config/torrc"])

        with open(os.path.join(service_dir, "hostname"), "r") as file:
            hostname = file.read().strip()
        
        return hostname
    except Exception as e:
        print(f"Erro ao gerar o serviço .onion: {e}")
        return None

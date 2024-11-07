import os
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_onion_service(port):
    try:
        # Define the configuration directory with absolute path
        base_dir = os.path.abspath("src/onyconnect/config")
        service_dir = os.path.join(base_dir, "hidden_service")
        
        # Create the directory for the .onion service with correct permissions
        logging.info("Creating directory for the .onion service.")
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)
        
        # Prepare torrc configuration
        logging.info("Reading and configuring the torrc template.")
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=service_dir)
        
        # Save torrc configuration
        torrc_path = os.path.join(base_dir, "torrc")
        logging.info(f"Saving torrc configuration at {torrc_path}.")
        with open(torrc_path, "w") as file:
            file.write(torrc_content)

        # Start Tor process with the customized torrc
        logging.info("Starting Tor process.")
        tor_process = subprocess.Popen(["tor", "-f", torrc_path])
        
        # Wait and check for hostname file to be created
        hostname_path = os.path.join(service_dir, "hostname")
        timeout = 20  # Timeout increased for safety
        for _ in range(timeout):
            if os.path.exists(hostname_path):
                logging.info("Hostname file found. Reading hostname.")
                with open(hostname_path, "r") as file:
                    hostname = file.read().strip()
                tor_process.terminate()
                return hostname
            logging.info("Waiting for hostname file to be created...")
            time.sleep(1)
        
        # If hostname file is not created within the timeout period
        logging.error("Hostname file not found. Terminating Tor process.")
        tor_process.terminate()
        raise FileNotFoundError("Hostname file not found. Check Tor's permissions and configuration.")
    
    except Exception as e:
        logging.error(f"Error generating the .onion service: {e}")
        return None

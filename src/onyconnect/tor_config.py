import os
import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_onion_service(port):
    try:
        # Define the configuration directory with absolute path
        base_dir = os.path.abspath("src/onyconnect/config")
        service_dir = os.path.join(base_dir, "hidden_service")
        
        # Create the directory for the .onion service with correct permissions
        logging.info("Creating directory for the .onion service.")
        os.makedirs(service_dir, exist_ok=True)
        os.chmod(service_dir, 0o700)  # Restricted permissions for Tor
        
        # Read the torrc template and insert the necessary variables
        logging.info("Reading and configuring the torrc template.")
        with open("src/onyconnect/config/torrc_template", "r") as file:
            torrc_content = file.read().format(port=port, directory=service_dir)
        
        # Save the content in the torrc file
        torrc_path = os.path.join(base_dir, "torrc")
        logging.info(f"Saving torrc configuration at {torrc_path}.")
        with open(torrc_path, "w") as file:
            file.write(torrc_content)

        # Start Tor with the specified torrc file
        logging.info("Starting Tor process.")
        tor_process = subprocess.Popen(["tor", "-f", torrc_path])

        # Wait to ensure Tor has time to generate the hostname
        time.sleep(5)

        # Check if the hostname file has been created
        hostname_path = os.path.join(service_dir, "hostname")
        if os.path.exists(hostname_path):
            logging.info("Hostname file found. Reading hostname.")
            with open(hostname_path, "r") as file:
                hostname = file.read().strip()
            # Terminate the Tor process after generating the hostname
            logging.info("Hostname generated successfully. Terminating Tor process.")
            tor_process.terminate()
            return hostname
        else:
            # Terminate the Tor process in case of error
            logging.error("Hostname file not found. Terminating Tor process.")
            tor_process.terminate()
            raise FileNotFoundError("Hostname file not found. Check Tor's permissions and configuration.")
    except Exception as e:
        logging.error(f"Error generating the .onion service: {e}")
        return None

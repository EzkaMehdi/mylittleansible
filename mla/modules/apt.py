import logging
from .base import BaseModule
from ssh_client import SSHClient

class AptModule(BaseModule):
    def __init__(self, ssh_client: SSHClient, **params):
        super().__init__(ssh_client, **params)
        self.ssh_client = ssh_client

    def execute(self):
        logging.info(f"Attempting to connect to SSH for host {self.ssh_client.host}")
        if not self.ssh_client.connect():
            logging.error("SSH connection could not be established.")
            return "SSH connection could not be established."

        try:
            # Building the command based on whether we are installing or removing a package
            action = 'install' if self.params['state'] == 'present' else 'remove'
            command = f"apt-get {action} -y {self.params['name']}"
            logging.info(f"Executing command on host {self.ssh_client.host}: {command}")
            
            stdout, stderr = self.ssh_client.execute_command(command)
            
            # Log any errors and return them
            if stderr:
                logging.error(f"Error during {action} of package {self.params['name']} on {self.ssh_client.host}: {stderr}")
                return f"Error: {stderr}"
            
            # Log successful execution
            logging.info(f"Successfully executed {action} command for {self.params['name']} on {self.ssh_client.host}: {stdout}")
            return stdout
        finally:
            logging.info(f"Closing SSH connection for host {self.ssh_client.host}")
            self.ssh_client.close()


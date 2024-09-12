from ssh_client import SSHClient
from .base import BaseModule

class ServiceModule(BaseModule):
    def init(self, ssh_client, params):
        super().init(ssh_client, params)
        self.ssh_client = ssh_client

    def execute(self):
        if not self.ssh_client.connect():
            return "SSH connection could not be established."

        try:
            # Utilisation de 'service' au lieu de 'systemctl'
            command = f"service {self.params['name']} {self.params['state']}"
            stdout, stderr = self.ssh_client.execute_command(command)
            if stderr:
                return f"Error: {stderr}"
            return stdout
        finally:
            self.ssh_client.close()
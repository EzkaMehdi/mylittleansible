from ssh_client import SSHClient
from .base import BaseModule

class CommandModule(BaseModule):
    def __init__(self, ssh_client, **params):
        super().__init__(ssh_client, **params)
        self.ssh_client = ssh_client

    def execute(self):
        if not self.ssh_client.connect():
            return "SSH connection could not be established."

        try:
            stdout, stderr = self.ssh_client.execute_command(self.params['cmd'])
            if stderr:
                return f"Error: {stderr}"
            return stdout
        finally:
            self.ssh_client.close()

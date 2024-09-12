import paramiko

class SSHClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        """Établit une connexion SSH au serveur distant."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials.")
            return False
        except paramiko.SSHException as e:
            print(f"Unable to establish SSH connection: {str(e)}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            return False
        return True

    def open_sftp(self):
        """Ouvre une session SFTP pour le transfert de fichiers."""
        try:
            self.sftp = self.client.open_sftp()
        except Exception as e:
            print(f"Failed to open SFTP session: {str(e)}")
            return None
        return self.sftp

    def close(self):
        """Ferme la connexion SSH et SFTP si ouvert."""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()

    def execute_command(self, command):
        """Exécute une commande sur le serveur distant et retourne la sortie."""
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

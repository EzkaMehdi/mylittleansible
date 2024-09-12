import os
import logging
from ssh_client import SSHClient
from .base import BaseModule

class CopyModule(BaseModule):
    def __init__(self, ssh_client, src, dest, backup=False):
        self.ssh_client = ssh_client
        self.src = src
        self.dest = dest
        self.backup = backup

    def execute(self):
        """Exécute la tâche de copie de fichiers."""
        logging.info(f"Attempting to connect SSH to copy from {self.src} to {self.dest}")
        if not os.path.isfile(self.src):
            logging.error(f"Source file {self.src} does not exist")
            return False

        if self.ssh_client.connect():
            sftp = self.ssh_client.open_sftp()
            if sftp:
                try:
                    # Gérer la sauvegarde si nécessaire
                    if self.backup:
                        try:
                            sftp.stat(self.dest)
                            remote_backup_path = f"{self.dest}.bak"
                            sftp.rename(self.dest, remote_backup_path)
                            logging.info(f"Backup created at {remote_backup_path}")
                        except IOError:
                            logging.warning(f"No file exists at {self.dest} to back up.")

                    # Exécution de la copie du fichier
                    logging.info(f"Attempting to copy file from {self.src} to {self.dest}")
                    sftp.put(self.src, self.dest)
                    logging.info(f"File copied successfully from {self.src} to {self.dest}")
                    return True
                except Exception as e:
                    logging.error(f"Failed to copy file: {e}")
                    return False
                finally:
                    sftp.close()
            self.ssh_client.close()
        else:
            logging.error("Failed to connect via SSH.")
        return False

    def file_exists(self, sftp, path):
        """Vérifie si un fichier existe sur le serveur distant."""
        try:
            sftp.stat(path)
            return True
        except IOError:
            logging.error(f"File at {path} not found on the server.")
            return False

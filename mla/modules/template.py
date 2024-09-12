import jinja2
import logging
from ssh_client import SSHClient
from .base import BaseModule

class TemplateModule(BaseModule):
    def init(self, ssh_client, params):
        super().init(ssh_client, params)
        self.ssh_client = ssh_client

    def execute(self):
        if not self.ssh_client.connect():
            return "SSH connection could not be established."

        try:
            template_path = self.params.get('template_path')
            if not template_path:
                raise ValueError("Template path not provided")
            logging.info(f"Loading templates from {template_path}")
            env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
            template = env.get_template(self.params['src'])
            logging.info(f"Rendering template {self.params['src']} with variables {self.params['vars']}")
            output = template.render(self.params['vars'])

            sftp = self.ssh_client.open_sftp()
            logging.info(f"Writing rendered template to {self.params['dest']} on remote host")
            with sftp.file(self.params['dest'], 'w') as f:
                f.write(output)
            sftp.close()
            return f"Template {self.params['src']} applied to {self.params['dest']}"
        except Exception as e:
            logging.error(f"Error applying template: {str(e)}")
            return f"Failed to apply template: {str(e)}"
        finally:
            self.ssh_client.close()
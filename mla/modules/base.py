class BaseModule:
    def __init__(self, ssh_client, **params):
        self.ssh_client = ssh_client
        self.params = params

    def validate(self):
        raise NotImplementedError("Must override validate to check parameters.")

    def execute(self):
        raise NotImplementedError("Must override execute to perform the module's task.")

import argparse
import yaml
import os
import logging
from ssh_client import SSHClient  
from modules.apt import AptModule
from modules.copy import CopyModule
from modules.service import ServiceModule
from modules.command import CommandModule
from modules.template import TemplateModule

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_yaml_file(filepath):
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return None

    with open(filepath, 'r') as file:
        try:
            data = yaml.safe_load(file)
            logging.info(f"Data loaded from {filepath}: {data}")  
            return data
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML file: {filepath}\n{e}")
            return None

def validate_data(data, required_keys):
    for item in data['tasks']: 
        for key in required_keys:
            if key not in item:
                logging.error(f"Missing required key '{key}' in item: {item}")
                return False
    return True

def execute_task(ssh_client, task):
    module_class = {
        'apt': AptModule,
        'copy': CopyModule,
        'service': ServiceModule,
        'template': TemplateModule,
        'command': CommandModule
    }.get(task['module'])

    if module_class:
        module = module_class(ssh_client, **task['params'])
        result = module.execute()
        ssh_client.close()
        return result
    return "Module not found or task parameters invalid."

def main():
    parser = argparse.ArgumentParser(description="MyLittleAnsible CLI tool")
    parser.add_argument('-f', '--file', type=str, required=True, help='Path to the todos YAML file')
    parser.add_argument('-i', '--inventory', type=str, required=True, help='Path to the inventory YAML file')
    args = parser.parse_args()

    todos = load_yaml_file(args.file)
    inventory = load_yaml_file(args.inventory)

    if todos is None or inventory is None or not validate_data(todos, ['module', 'params']):
        return

    for host_name, host_info in inventory['hosts'].items():
        ssh_client = SSHClient(
            host_info['ssh_address'],
            host_info['ssh_port'],
            host_info['ssh_user'],
            host_info['ssh_password']
        )
        if ssh_client.connect():
            for task in todos['tasks']: 
                logging.info(f"Executing task {task['module']} on host: {host_name}")
                result = execute_task(ssh_client, task)
                logging.info(f"Task on {host_name} completed with result: {result}")
        else:
            logging.error(f"Failed to connect to {host_name}")

if __name__ == "__main__":
    main()

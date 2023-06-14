import argparse
import json
import getpass
import os


def main():
    setup_config_file()

def setup_config_file():
    parser = argparse.ArgumentParser(description='Configuration File Setup')
    parser.add_argument('--addserver', action='store_true', help='Add a new server configuration')
    parser.add_argument('--list', action='store_true', help='List all servers')
    parser.add_argument('--setdefault', action='store_true', help='Set default values')
    parser.add_argument('--removeserver', help='Remove a server from the servers list')
    args = parser.parse_args()

    config = {}

    if not os.path.exists('config.json'):
        config['default'] = {
            'port': '',
            'username': '',
            'private_key': '',
            'public_key': ''
        }
        config['servers'] = []

    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
    
    if args.addserver:
        add_server_config(config)
    elif args.list:
        list_servers(config)
    elif args.setdefault:
        set_default_values(config)
    elif args.removeserver:
        remove_server_config(config, args.removeserver)
    else:
        print("Options:")
        parser.print_help()
        return

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def list_servers(config):
    servers = config.get('servers', [])
    if servers:
        print("Servers:")
        for server in servers:
            print(server)
    else:
        print("No servers found.")

def set_default_values(config):
    port = input("Enter default port: ")
    username = input("Enter default username: ")
    private_key_path = input("Enter default private key path: ")
    # Add additional fields as needed

    config['default']['port'] = port
    config['default']['username'] = username
    config['default']['private_key'] = private_key_path

def add_server_config(config):
    server_name = input("Enter server name: ")
    host = input("Enter host: ")
    port = input("Enter port(default:22): ")
    username = input("Enter username(optional): ")
    password = getpass.getpass("Password(optional): ")
    private_key_path = input("Enter private key path(optional): ")
    macaddress = input(("Enter MAC address(optional to wake-on-LAN): "))
    # Add additional fields as needed

    server_config = {
        'name': server_name,
        'host': host,
        'port': port,
        'username': username,
        'password': password,
        'private_key': private_key_path,
        'macaddress': macaddress
    }
    config['servers'].append(server_config)

def remove_server_config(config, server_name):
    servers = config.get('servers', [])
    for server in servers:
        if server['name'] == server_name:
            servers.remove(server)
            print(f"Server '{server_name}' removed.")
            return
    print(f"Server '{server_name}' not found.")

setup_config_file()
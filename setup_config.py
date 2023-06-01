import configparser
import os

def setup_config_file():
    config = configparser.ConfigParser()

    if not os.path.exists('config.ini'):
        menu = """Select the parameter you want to change:
        [1] Host
        [2] Port
        [3] Username
        [4] Private key path
        [5] Password
        [E] Everything
        """

        host = input("Enter host: ")
        port = input("Enter port: ")
        username = input("Enter username: ")
        private_key_path = input("Enter private key path: ")
        password = input("Enter password: ")

        choice = input(menu)

        if choice == '1' or choice == 'E':
            host = input("Enter host: ")
        if choice == '2' or choice == 'E':
            port = input("Enter port: ")
        if choice == '3' or choice == 'E':
            username = input("Enter username: ")
        if choice == '4' or choice == 'E':
            private_key_path = input("Enter private key path: ")
        if choice == '5' or choice == 'E':
            password = input("Enter password: ")

        config['SSH'] = {
            'host': host,
            'port': port,
            'username': username,
            'private_key_path': private_key_path,
            'password': password
        }

        with open('config.ini', 'w') as f:
            config.write(f)
    else:
        print("Config file already exists.")
        itens = config.read('config.ini')
        print(itens)
        

setup_config_file()
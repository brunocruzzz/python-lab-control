import paramiko
import getpass
import configparser

class SSHConfiguration:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.host = self.config['DEFAULT']['host']
        self.port = self.config.getint('DEFAULT', 'port')
        self.username = self.config['DEFAULT']['username']
        self.private_key_path = self.config['DEFAULT']['private_key_path']
        self.password = self.config['DEFAULT']['password']

    def get_password(self):
        if not self.password:
            self.password = getpass.getpass("Password: ")
        return self.password


class SSHClient:
    def __init__(self, config):
        self.config = config
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(
                hostname=self.config.host,
                username=self.config.username,
                password=self.config.get_password(),    
                port=self.config.port
            )
            print("Connected successfully!")
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as ssh_ex:
            print(f"Unable to establish SSH connection: {ssh_ex}")
        except Exception as ex:
            print(f"An error occurred: {ex}")

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        return f"{output}  -  {error}"

    def close(self):
        self.client.close()

def main():
    config = SSHConfiguration('config.ini')

    ssh = SSHClient(config)

    try:
        print(f"Trying to ssh {config.username}@{config.host}:{config.port}")
        ssh.connect()
        output = ssh.execute_command('hostname')
        print(output)
        while True:
            command = input("Enter a command to execute (type '!exit' to quit): ")
            if command == "!exit":
                break

            output = ssh.execute_command(command)
            print(output)

    finally:
        ssh.close()

    print("Connection ended.")


if __name__ == '__main__':
    main()
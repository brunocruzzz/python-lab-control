import paramiko
import os, subprocess
import getpass

import json

class SSHConfiguration:
    def __init__(self, config_file):        
        if not os.path.exists(config_file):
            print("Config file does not exist. Running setup script...")
            subprocess.call(['python', 'setup_config.py', '--addserver'])
            # Add any necessary logic after running the setup script
        
        with open(config_file, 'r') as f:
            config = json.load(f)    
        self._default_config = config['default']
        self._servers = config.get('servers', [])

        if not self._servers:
            print("Warning: No server host configuration loaded!")           
            self._current_config = self._default_config
        else:
            num_servers = len(self._servers)            
            self._current_config = self._servers[0]

    def get_password(self):
        if not self.password:
            self.password = getpass.getpass("Password: ")
        return self.password
    
    @property
    def port(self):
        return self._port

    @property
    def username(self):
        return self._username

    @property
    def private_key_path(self):
        return self._private_key_path


    @property
    def servers(self):
        return self._servers

class SSHClient:
    def __init__(self, config):        
        self.config = config        
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())              
    
    def connect(self,server):                  
        try:
            self.client.connect(
                hostname=server['host'],
                username=server['username'],
                password=server['password'],
                port=server['port']
            )
            print("Connected successfully!")
        except paramiko.AuthenticationException:
            print("Authentication failed. Please check your credentials.")
        except paramiko.SSHException as ssh_ex:
            print(f"Unable to establish SSH connection: {ssh_ex}")
        except Exception as ex:
            print(f"An error occurred: {ex}")
            raise  # Re-raise the exception to halt execution
            

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if error:
                return f"Error executing command: {error}"
            elif output:
                #return output.strip()  # Remove leading/trailing whitespace
                return output
            else:
                return "No output available."
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def close(self):
        self.client.close()

def select_server(config):    
    if len(config.servers) > 1:
        print(f"{len(config.servers)} servers. Please choose a server to connect: ")        
        print(f"|---SERVERS {'-'*80}|")        
        for i, server in enumerate(config.servers):
            print(f"[{i+1}] {server['name']} ({server['host']}:{server['port']})")
        print(f"|---OPTIONS {'-'*80}|")
        print(f"[*] Choose to run in all servers - (choose it wisely!)")
        print(f"[+] Add new server [R] Remove server [E] Edit server")
        print(f"[x] Exit")
        choice = input("Enter the server number/option: ")
        if choice =='x':
            exit("Python-Lab-Control Terminated.")
        elif choice =='+':
            #call setup_config in run-time to fill and reload config file.
            subprocess.call(['python', './setup_config.py', '--addserver'])
            return(select_server(config))
        elif choice =='R':            
            remoserver = input("Enter the server number: ")
            removed_item = config.servers.pop(int(remoserver)-1)['name']
            confirmation = input(f"Confirme item to remove? --> {removed_item} (Y/N): ").lower()
            if confirmation == 'y':
                #call setup_config in run-time to fill and reload config file.
                subprocess.call(['python', './setup_config.py', f"--removeserver", f"{removed_item}"])
            #Reload written configuration
            config = SSHConfiguration('config.json')
            return(select_server(config))
        try:
            choice = int(choice)
            if 1 <= choice <= len(config.servers):
                server = config.servers[choice-1]
            else:
                print("Invalid server number. Exiting.")
                return None
        except ValueError:
            print("Invalid input. Exiting.")
            return None
    elif len(config.servers) == 1:        
        server = config.servers[0]        
    else:
        print("No servers found in the configuration.")
        handle = input("[+] Add new server / [x] Exit")
        if handle =='+':
            #call setup_config in run-time to fill and reload config file.
            subprocess.call(['python', './setup_config.py', '--addserver'])
        if handle =='x':
            exit
        #elif handle =='-':
        #elif handle =='e':
        
        config = SSHConfiguration('config.json')
        return select_server(config)

    return server

def main():
    print("PythonSSH Lab Control - Version 0.2")
    print("+----------------------------------+")
    print("|   Initializing SSH Connection    |")
    print("+----------------------------------+")
    # Read configuration
    print("Reading configuration...")
    config = SSHConfiguration('config.json')
    ssh = SSHClient(config)
    while True:
        server = select_server(config)
        if not server:
            break
        #print(config._default_config)
        #print(server)
        print(f"Trying to SSH {server['username']}@{server['host']}:{server['port']}")
        try:              
            #With the following 2 lines, with connect to server and print its hostname
            ssh.connect(server)
            output = ssh.execute_command('hostname')
            print(output)
            print(f"Enter a command to execute (type '!exit' to quit(Or ? to show all local options...))")
            
            while True:
                command = input(f"{server['username']}@{server['host']}: ")
                if command == "!exit":
                    break
                elif command == "!pubkey":
                    print('Em implementação')
                #command = f"printf 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCi6K02jP5EAwCClQepmgoD6ru/Xs1C55KyOAuWDMptDX+ovM8WTsFeYMBB2gV6r1iTcD0ablqLRaEVRVKH669pztekbNcM+LfoJqWO9Lnv/QCJeC8qdqDpT0ZuS+3WyvW6sJ0MAKxR9Y5AOw49zx94IXJLMzNKUH7QlW8GS1wO17nP+uJlQAaKgFkAiQZjb4767t5sh311lj7sywdLvXrT22HEfBgWhKVPA1xUIdD+pPHSv1e+alV47TdQPIt5ABdmX4MxfKS/dyWu+OGkwDq6+++B+SFywej8rLhyRhxCY3F4ZH+xt6ZHahgiPA/N5PQ+DM0ZwHhtuDLpdtjfM7Gx\n' >> ~/.ssh/authorized_keys"
                elif command == '!--addserver':
                    print('Abrindo configurador para registrar novo servidor--->Em implementação')
                    subprocess.call(['python', './setup_config.py', '--addserver'])
                    config = SSHConfiguration('config.json')
                    continue
                elif command =='!su':
                    print("Implementação futura...")
                else:
                    output = ssh.execute_command(command)
                    print(output)
        except:
            print("Can't connect to server.")
        finally:
            ssh.close()
            print("+----------------------------------+")
            print("|         Connection ended.        |") 
            print("+----------------------------------+")


if __name__ == '__main__':
    main()
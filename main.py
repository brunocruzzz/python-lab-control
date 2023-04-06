import paramiko
import getpass
# specify the host information
host = ""
port = 22
username = ""
passwd = getpass.getpass("Password: ")

ssh = paramiko.SSHClient()
print(f"Trying to --> ssh {username}@{host}:{port}")
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=host, username=username, password=passwd,port=port)

stdin, stdout, stderr = ssh.exec_command('ls -l')
output = stdout.readlines()

# print the output of the command
print(output)


#Messages and ends the connection
print("Connection ended.")
ssh.close()
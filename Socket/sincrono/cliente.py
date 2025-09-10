import socket
import pickle
import struct
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from Utils import Utils
class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_line_column(self, line: list, column: list) -> int:
       
        data = pickle.dumps((line, column))
        data_len = struct.pack('>I', len(data))  

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data_len)
            s.sendall(data)

            raw_msglen = s.recv(4)
            if not raw_msglen:
                raise ConnectionError("Servidor fechou a conexão.")
            msglen = struct.unpack('>I', raw_msglen)[0]

            response_data = b''
            while len(response_data) < msglen:
                packet = s.recv(4096)
                if not packet:
                    raise ConnectionError("Conexão interrompida pelo servidor.")
                response_data += packet

            result = pickle.loads(response_data)
            return result

if __name__ == "__main__":
    client = Client("172.17.0.1", 5000)

    MatrizA = [[i for i in range(10)] for _ in range(10)]
    MatrizB = [[i for i in range(10)] for _ in range(10)]
    MatrizC = []

    for i in range(len(MatrizA)):
        newLineC = []
        for j in range(len(MatrizB[0])):  
            columnB = Utils.getColumn(MatrizB, j)
            result = client.send_line_column(MatrizA[i], columnB)
            newLineC.append(result)
        MatrizC.append(newLineC) 

    for line in MatrizC:
        print(line)

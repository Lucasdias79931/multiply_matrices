import socket
import pickle
import struct
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Client_base import Client_base
from Utils import Utils

class Client(Client_base):
    
    def send_line_column(self, line: list, column: list):
        """
        Send line and column to the server, receive response dict:
        { "status": "ok", "result": value } or { "status": "error", "message": str }
        """
        data = pickle.dumps((line, column))
        data_len = struct.pack('>I', len(data))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(data_len)
            s.sendall(data)

            # receive 4-byte header
            raw_msglen = s.recv(4)
            if not raw_msglen:
                raise  ("Server closed the connection.")
            msglen = struct.unpack('>I', raw_msglen)[0]

            # receive response body
            response_data = b''
            while len(response_data) < msglen:
                packet = s.recv(4096)
                if not packet:
                    raise ConnectionError("Connection interrupted by the server.")
                response_data += packet

            # deserialize dict
            response = pickle.loads(response_data)

            if not isinstance(response, dict):
                raise ValueError("Invalid response format from server")

            if response.get("status") == "ok":
                return response["result"]
            else:
                # raise error with message from server
                raise ValueError(f"Server error: {response.get('message')}")

    def multiply_matrices(self, MatrizA, MatrizB):
        MatrizC = []

        for i in range(len(MatrizA)):
            results = []
            for j in range(len(MatrizB[0])):
                columnB = Utils.getColumn(MatrizB, j)
                try:
                    result = self.send_line_column(MatrizA[i], columnB) 
                except Exception:
                    result = None
                results.append(result)
            MatrizC.append(results)
            
            

        return MatrizC

if __name__ == "__main__":

    from Utils import Utils
    client = Client("localhost", 5002)

    MatrizA = [[1,2],[3,4]]
    MatrizB = [[5,6],[7,8]]
    MatrizC = client.multiply_matrices(MatrizA, MatrizB)

   
   
    for line in MatrizC:
        print(line)

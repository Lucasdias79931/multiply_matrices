import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import grpc
import matrix_pb2
import matrix_pb2_grpc
from Utils import Utils
from Client_base import Client_base

class GRPCClient(Client_base):
    def __init__(self, host="localhost", port=50051):
        super().__init__(host, port)
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = matrix_pb2_grpc.MatrixServiceStub(channel)

    def send_line_column(self, line, column):
        request = matrix_pb2.LineColumn(line=line, column=column)
        response = self.stub.Multiply(request)
        if response.status == "ok":
            return response.value   

        else:
            raise ValueError(f"Server error: {response.message}")

    def multiply_matrices(self, MatrizA, MatrizB):
        MatrizC = []
        for i in range(len(MatrizA)):
            row = []
            for j in range(len(MatrizB[0])):
                colB = Utils.getColumn(MatrizB, j)
                row.append(self.send_line_column(MatrizA[i], colB))
            MatrizC.append(row)
        return MatrizC
    
    


if __name__ == "__main__":
    
    client = GRPCClient()
    MatrizA = [[1,2],[3,4]]
    MatrizB = [[5,6],[7,8]]
    matrix10 = [[[i*2 for i in range(10)] for _ in range(10)] for _ in range(2)]

    MatrizB = [[5,6],[7,8]]
    C = client.multiply_matrices(matrix10[0], matrix10[1])
    
    for line in C:
        print(line)

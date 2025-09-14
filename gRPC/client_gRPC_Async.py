import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import grpc
import matrix_pb2
import matrix_pb2_grpc
from Utils import Utils
from Client_base import Client_base
import asyncio

class GRPCClientAsync(Client_base):
    def __init__(self, host="localhost", port=50051):
        super().__init__(host, port)
        self.host = host
        self.port = port

    async def send_line_column(self, stub, line, column):
        request = matrix_pb2.LineColumn(line=line, column=column)
        response = await stub.Multiply(request)
        if response.status == "ok":
            return response.value
        else:
            raise ValueError(f"Server error: {response.message}")

    async def multiply_matrices(self, MatrizA, MatrizB):
        async with grpc.aio.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = matrix_pb2_grpc.MatrixServiceStub(channel)

            MatrizC = []
            for i in range(len(MatrizA)):
                tasks = []
                for j in range(len(MatrizB[0])):
                    colB = Utils.getColumn(MatrizB, j)
                    tasks.append(self.send_line_column(stub, MatrizA[i], colB))

                results = await asyncio.gather(*tasks, return_exceptions=True)
                MatrizC.append([r if not isinstance(r, Exception) else None for r in results])

            return MatrizC


if __name__ == "__main__":
    client = GRPCClientAsync()
    MatrizA = [[1,2],[3,4]]
    MatrizB = [[5,6],[7,8]]
    C = asyncio.run(client.multiply_matrices(MatrizA, MatrizB))

    for line in C:
        print(line)

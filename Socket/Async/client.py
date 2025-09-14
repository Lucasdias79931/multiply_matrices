import asyncio
import struct
import pickle
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Client_base import Client_base

from Utils import Utils

class AsyncClient(Client_base):

    async def send_line_column(self, line: list, column: list):
        """Send line and column to the async server and receive response."""
        reader, writer = await asyncio.open_connection(self.host, self.port)

        # Serialize payload
        data = pickle.dumps((line, column))
        data_len = struct.pack('>I', len(data))
        writer.write(data_len + data)
        await writer.drain()

        # Receive 4-byte header
        raw_msglen = await reader.readexactly(4)
        msglen = struct.unpack('>I', raw_msglen)[0]

        # Receive response
        response_data = await reader.readexactly(msglen)
        response = pickle.loads(response_data)

        writer.close()
        await writer.wait_closed()

        if not isinstance(response, dict):
            raise ValueError("Invalid response format from server")
        if response.get("status") == "ok":
            return response["result"]
        else:
            raise ValueError(f"Server error: {response.get('message')}")
    
    async def multiply_matrices(self, MatrizA, MatrizB):
        MatrizC = []
        
        for i in range(len(MatrizA)):
            tasks = []
            for j in range(len(MatrizB[0])):
                columnB = Utils.getColumn(MatrizB, j)
                tasks.append(self.send_line_column(MatrizA[i], columnB))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            MatrizC.append([r if not isinstance(r, Exception) else None for r in results])
        return MatrizC

if __name__ == "__main__":
    client = AsyncClient("localhost", 5002)
    
    MatrizA = [[1,2],[3,4]]
    MatrizB = [[5,6],[7,8]]

    MatrizC = asyncio.run(client.multiply_matrices(MatrizA, MatrizB))

    for line in MatrizC:
        print(line)
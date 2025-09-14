import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import struct
import pickle
import traceback
from Utils import Utils
import asyncio
from Server_base import ServerBase

class ServerAsync(ServerBase):
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"[+] New connection from {addr}")
        
        await self.escalarM(reader, writer)
        writer.close()
        await writer.wait_closed()

    async def connect(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        addr = server.sockets[0].getsockname()
        print(f"[+] Async server listening on {addr}")

        async with server:
            await server.serve_forever()

    async def escalarM(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        try:
            # Read 4-byte length header
            raw_msglen = await reader.readexactly(4)
            msglen = struct.unpack('>I', raw_msglen)[0]

            # Read the message body
            data = await reader.readexactly(msglen)

            # Deserialize payload
            payload = pickle.loads(data)

            # Support either dict {"line":..., "column":...} or tuple/list (line, column)
            if isinstance(payload, dict) and 'line' in payload and 'column' in payload:
                line = payload['line']
                column = payload['column']
            elif isinstance(payload, (list, tuple)) and len(payload) == 2:
                line, column = payload
            else:
                raise ValueError("Invalid payload format")

            # Validate line and column
            if not isinstance(line, (list, tuple)) or not isinstance(column, (list, tuple)):
                raise ValueError("line and column must be lists or tuples")
            if len(line) != len(column):
                raise ValueError(f"Incompatible sizes: line={len(line)}, column={len(column)}")

            # Compute dot product
            result = Utils.scalarMultiply(line, column)
            resp = {'status': 'ok', 'result': result}

        except Exception as e:
            resp = {'status': 'error', 'message': str(e)}
            print(f"[!] Error in escalarM: {e}")
            traceback.print_exc()

        # Send response
        resp_bytes = pickle.dumps(resp)
        writer.write(struct.pack('>I', len(resp_bytes)) + resp_bytes)
        await writer.drain()

if __name__ == "__main__":
    server = ServerAsync("0.0.0.0", 5002)
    try:
        asyncio.run(server.connect())
    except KeyboardInterrupt:
        print("\n[+] Server stopped manually")

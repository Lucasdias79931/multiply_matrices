import sys
import socket
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from Utils import Utils
from Server_base import ServerBase
import traceback
import pickle
import struct

import socket

class ServerSync(ServerBase):
    def connect(self):
       
       
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"[+] Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                print(f"[+] New connection from {addr}")
                with conn:
                    self.escalarM(conn)

    def escalarM(self, conn):
        """
        Receive a pickled payload (4-byte length header + payload),
        unpack (line, column), compute dot product and send a pickled
        response dict: {'status':'ok','result':int} or {'status':'error','message':str}.
        """
        try:
            # read 4 bytes length header
            raw_msglen = conn.recv(4)
            if not raw_msglen:
                return
            msglen = struct.unpack('>I', raw_msglen)[0]

            # read message body
            data = b''
            while len(data) < msglen:
                packet = conn.recv(4096)
                if not packet:
                    raise ConnectionError("Connection closed while receiving payload")
                data += packet

            # deserialize payload
            try:
                payload = pickle.loads(data)
                
                if isinstance(payload, dict) and 'line' in payload and 'column' in payload:
                    line = payload['line']
                    column = payload['column']
                elif isinstance(payload, (list, tuple)) and len(payload) == 2:
                    line, column = payload
                else:
                    raise ValueError("Invalid payload format: expected (line, column) or {'line':..., 'column':...}")
            except Exception as e:
                resp = {'status': 'error', 'message': f'Invalid payload: {e}'}
                self._send_response(conn, resp)
                return

            #
            if not isinstance(line, (list, tuple)) or not isinstance(column, (list, tuple)):
                resp = {'status': 'error', 'message': 'line and column must be lists or tuples'}
                self._send_response(conn, resp)
                return

            if len(line) != len(column):
                resp = {'status': 'error', 'message': f'Incompatible sizes: line={len(line)} column={len(column)}'}
                self._send_response(conn, resp)
                return

            
            try:
                result = Utils.scalarMultiply(line, column)
                resp = {'status': 'ok', 'result': result}
            except Exception as e:
                resp = {'status': 'error', 'message': str(e)}

            
            self._send_response(conn, resp)

        except Exception as e:
            
            print(f"[!] Unexpected error in escalarM: {e}")
            traceback.print_exc()
            try:
                self._send_response(conn, {'status': 'error', 'message': 'internal server error'})
            except Exception:
                pass
if __name__ == "__main__":
    server = ServerSync("0.0.0.0", 5001)
    server.connect()

import sys
import os
import pickle
import struct
import traceback

from Utils import Utils
from abc import ABC, abstractmethod


class ServerBase(ABC):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @abstractmethod
    def connect(self):
        """Must be implemented by subclasses (sync/async)."""
        pass
    
    @abstractmethod
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
                # support either (line, column) tuple/list or {"line":..., "column":...}
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

            # validate sizes explicitly
            if not isinstance(line, (list, tuple)) or not isinstance(column, (list, tuple)):
                resp = {'status': 'error', 'message': 'line and column must be lists or tuples'}
                self._send_response(conn, resp)
                return

            if len(line) != len(column):
                resp = {'status': 'error', 'message': f'Incompatible sizes: line={len(line)} column={len(column)}'}
                self._send_response(conn, resp)
                return

            # compute dot product (rely on Utils)
            try:
                result = Utils.escalarMultiply(line, column)
                resp = {'status': 'ok', 'result': result}
            except Exception as e:
                resp = {'status': 'error', 'message': str(e)}

            # send response
            self._send_response(conn, resp)

        except Exception as e:
            # unexpected error: try to respond and log
            print(f"[!] Unexpected error in escalarM: {e}")
            traceback.print_exc()
            try:
                self._send_response(conn, {'status': 'error', 'message': 'internal server error'})
            except Exception:
                pass

    def _send_response(self, conn, obj):
        """Helper: pickle obj, send 4-byte length header + payload"""
        b = pickle.dumps(obj)
        header = struct.pack('>I', len(b))
        conn.sendall(header + b)

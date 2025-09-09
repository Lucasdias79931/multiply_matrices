import sys
import Socket
import os
import pickle
import struct
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from Utils import Utils
from abc import ABC, abstractmethod



class ServerBase(ABC):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @abstractmethod
    def conect(self):
        """Método para aceitar conexões (implementação depende do tipo de servidor)."""
        pass

    def escalarM(self, conn):
        """
        Recebe linha e coluna do cliente, calcula o produto escalar
        e envia o resultado de volta.
        Suporta listas grandes enviadas em pacotes.
        """
        try:
            # Recebe primeiro 4 bytes com o tamanho da mensagem
            raw_msglen = conn.recv(4)
            if not raw_msglen:
                return
            msglen = struct.unpack('>I', raw_msglen)[0]

            # Recebe todos os bytes da mensagem
            data = b''
            while len(data) < msglen:
                packet = conn.recv(4096)
                if not packet:
                    return
                data += packet

            # Desserializa linha e coluna
            line, column = pickle.loads(data)

            # Calcula produto escalar
            result = Utils.escalarMultiply(line, column)

            # Envia resultado de volta
            result_bytes = pickle.dumps(result)
            result_len = struct.pack('>I', len(result_bytes))
            conn.sendall(result_len)
            conn.sendall(result_bytes)

        except Exception as e:
            print(f"[!] Erro no cálculo escalar: {e}")

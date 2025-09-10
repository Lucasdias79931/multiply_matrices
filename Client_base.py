import socket
import pickle
import struct


from Utils import Utils
from abc import ABC, abstractmethod

__all__ = ['Client_base']

class Client_base(ABC):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @staticmethod
    def send_line_column(self, line: list, column: list):
        pass





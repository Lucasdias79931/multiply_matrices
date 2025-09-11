"""
    This module was created to test performance utilizing different methods of inter-process communication.

    The methods tested are:
    - Sockets (synchronous and asynchronous)
    - gRPC
"""


import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../gRPC')))
from Utils import Utils
import asyncio
from Socket.sincrono.client import Client as SyncClient
from Socket.Async.client import AsyncClient
from gRPC.client_gRPC import GRPCClient






Cliets = {
    "Socket Sincrono": SyncClient("0.0.0.0", 5000),
    "Socket Assincrono": AsyncClient("0.0.0.0", 5001),
    "gRPC": GRPCClient()
}

def test(MatrixA, MatrixB, client, method_name):
    start_time = time.time()
    MatrixC = client.multiply_matrices(MatrixA, MatrixB)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"method": method_name, "time": elapsed_time}

df = pd.DataFrame(columns=["Size_matrices","method", "time"])

matrix10 = [[[i*2 for i in range(10)] for _ in range(10)] for _ in range(2)]
matrix100 = [[[i*2 for i in range(100)] for _ in range(100)] for _ in range(2)]
matrix1000 = [[[i*2 for i in range(1000)] for _ in range(1000)] for _ in range(2)]

print("Testing with 10x10 dot 10X10 matrices")
for method_name, client in Cliets.items():
    result = test(matrix10[0], matrix10[1], client, method_name)
    result["Size_matrices"] = "10x10 dot 10x10"
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    print(f"{method_name}: {result['time']:.4f} seconds")

print(df.head())
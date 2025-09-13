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
import inspect
import asyncio
from Socket.sincrono.client import Client as SyncClient
from Socket.Async.client import AsyncClient
from gRPC.client_gRPC import GRPCClient






Cliets = {
    "Socket Sincrono": SyncClient("192.168.1.160", 5002),
    "Socket Assincrono": AsyncClient("192.168.1.160", 5001),
    "gRPC": GRPCClient(host="192.168.1.160")
}


def test(MatrixA, MatrixB, client, method_name):
    start_time = time.time()
    

    if inspect.iscoroutinefunction(client.multiply_matrices):
        MatrixC = asyncio.run(client.multiply_matrices(MatrixA, MatrixB))
    else:
        MatrixC = client.multiply_matrices(MatrixA, MatrixB)

    end_time = time.time()
    elapsed_time = end_time - start_time
    return {"method": method_name, "time": elapsed_time}


df = pd.DataFrame(columns=["Size_matrices","method", "time"])

matrix10 = [[[i*2 for i in range(10)] for _ in range(10)] for _ in range(2)]
matrix50 = [[[i*2 for i in range(50)] for _ in range(50)] for _ in range(2)]
matrix100 = [[[i*2 for i in range(100)] for _ in range(100)] for _ in range(2)]




for method_name, client in Cliets.items():
    
    result = test(matrix10[0], matrix10[1], client, method_name)
    result["Size_matrices"] = "10x10 dot 10x10"
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    print(f"{method_name}: {result['time']:.4f} seconds")

    result = test(matrix50[0], matrix50[1], client, method_name)
    result["Size_matrices"] = "50x50 dot 50x50"
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    print(f"{method_name}: {result['time']:.4f} seconds")

    result = test(matrix100[0], matrix100[1], client, method_name)
    result["Size_matrices"] = "100x100 dot 100x100"
    df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)
    print(f"{method_name}: {result['time']:.4f} seconds")

    
    

df.to_csv("performance_results.csv", index=False)


# Plotando resultados
plt.figure(figsize=(10, 6))

# gráfico de barras agrupadas
for i, size in enumerate(df["Size_matrices"].unique()):
    subset = df[df["Size_matrices"] == size]
    plt.bar(
        [x + i*0.25 for x in range(len(subset))],  # desloca cada grupo
        subset["time"],
        width=0.25,
        label=size
    )

plt.xticks(range(len(df["method"].unique())), df["method"].unique())
plt.ylabel("Tempo (segundos)")
plt.title("Comparação de métodos de comunicação")
plt.legend(title="Tamanho da matriz")
plt.tight_layout()
plt.savefig("performance_comparison.png")
plt.show()


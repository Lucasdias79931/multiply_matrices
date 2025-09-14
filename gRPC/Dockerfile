FROM python:3.12-slim

WORKDIR /app

# Copia o requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos que todos os servidores precisam
COPY Utils.py .
COPY Client_base.py .
COPY Server_base.py .

# Copia o código do servidor
COPY gRPC/ gRPC/

EXPOSE 50051
CMD ["python3", "gRPC/server_gRPC.py"]
# Comando para rodar o servidor
# docker run -p 50051:50051 grpc_server
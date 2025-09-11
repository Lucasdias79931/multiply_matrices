FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Utils.py .
COPY Client_base.py .
COPY Server_base.py .
COPY Socket/sincrono/ Socket/sincrono/

EXPOSE 5000
CMD ["python", "Socket/sincrono/server.py"]

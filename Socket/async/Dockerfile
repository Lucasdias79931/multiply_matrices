FROM python:3.12-slim

WORKDIR /app

# ---------- Instala dependências de sistema ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/*



COPY . .

# ---------- Expõe a porta da aplicação ----------
EXPOSE 5000

# ---------- Comando para iniciar a aplicação ----------
CMD ["python3", "-u", "server.py"]



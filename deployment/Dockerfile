# Usa imagen oficial de Python 3.11.10 slim
FROM python:3.11.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# ⬇️ Añade libpq-dev para compilar psycopg2
RUN apt-get update && \
    apt-get install -y ffmpeg libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . /app

# Instala dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8000 (usado por Uvicorn)
EXPOSE 8000

# Comando que inicia FastAPI
CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la API y el modelo
COPY . .

# Exponer el puerto de la API
EXPOSE 8000

# Comando para iniciar el servidor
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
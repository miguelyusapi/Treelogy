# Imagen base
FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gnupg \
    curl \
    unixodbc-dev \
    libodbc1 \
    odbcinst \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY ./app/ /app/

# Exponer el puerto del backend
EXPOSE 8000

# Cambiar el comando para ejecutar el main.py dentro de app/version1/ventas
CMD ["uvicorn", "version1.ventas.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

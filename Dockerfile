# Imagen base
FROM python:3.11-slim


# Prerequisitos para el driver ODBC
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl apt-transport-https gnupg \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/11/prod.list \
      > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev \
 && rm -rf /var/lib/apt/lists/*

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
CMD ["uvicorn", "version1.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Python estable compatible con Pillow
FROM python:3.12-slim

# Evitar creación de archivos .pyc y usar buffer normal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalación de dependencias del sistema para Pillow y MySQL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean

# Crear directorio de la app
WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Puerto del backend
EXPOSE 8000

# Comando para correr Django
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Usa la imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia solo los archivos necesarios al contenedor
COPY . /app

# Crear directorios necesarios
RUN mkdir -p /app/logs

# Asegurar que tenga permisos de ejecución
RUN chmod +x /app/entrypoint.sh

# Instala las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Configura el punto de entrada para iniciar el contenedor
ENTRYPOINT ["bash", "/app/entrypoint.sh"]

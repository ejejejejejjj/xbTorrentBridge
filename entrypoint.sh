#!/bin/bash

# Variables de entorno (pueden venir de docker-compose o ser definidas en el Dockerfile)
RSS_KEY=${RSS_KEY:-default_rss_key}
PORT=${PORT:-8080}

# Configuración inicial
echo "[INFO] RSS_KEY=$RSS_KEY"
echo "[INFO] PORT=$PORT"

# Ejecutar feeder.py como servicio en segundo plano
echo "[INFO] Iniciando feeder.py en segundo plano..."
nohup python3 /app/src/feeder.py > /app/logs/feeder.log 2>&1 &
FEEDER_PID=$!
echo $FEEDER_PID > /app/logs/feeder.pid
echo "[INFO] feeder.py iniciado con PID $FEEDER_PID"

# Bucle infinito para ejecutar downloader.py y key_updater.py cada 30 minutos
while true; do
    echo "[INFO] Ejecutando downloader.py y key_updater.py..."
    python3 /app/src/downloader.py >> /app/logs/downloader.log 2>&1
    python3 /app/src/key_updater.py >> /app/logs/downloader.log 2>&1
    echo "[INFO] Ejecución completada. Esperando 30 minutos..."
    sleep 1800  # Esperar 30 minutos
done

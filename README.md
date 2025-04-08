# xbTorrentBridge

xbTorrentBridge es un servicio basado en Python diseñado para procesar y gestionar feeds RSS personalizados. Este proyecto incluye varios scripts para automatizar tareas, como la descarga y actualización de claves RSS, con la capacidad de ejecutarse fácilmente dentro de un contenedor Docker.

## 🚀 Características

- Procesamiento y filtrado de feeds RSS mediante Python.
- Automatización de tareas periódicas con soporte para ejecución en segundo plano.
- Configuración simplificada a través de variables de entorno.
- Fácil integración y despliegue utilizando Docker y Docker Compose.

## 📋 Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu máquina:

- **Docker** (20.10 o superior)
- **Docker Compose** (1.29 o superior)

## 🛠️ Instalación

### Crear el Archivo docker-compose.yml

```yaml
version: "3.8"

services:
  xb-torrent-bridge:
    image: ejejejejejjj/xb-torrent-bridge:latest  # Imagen en Docker Hub
    container_name: xb-torrent-bridge            # Nombre del contenedor
    ports:
      - "8080:8080"                              # Mapea el puerto del contenedor al host
    environment:
      RSS_KEY: "mi_clave_rss"                    # Variable de entorno para RSS Key
      PORT: 8080                                 # Puerto que usará la aplicación
    volumes:
      - ./logs:/app/logs                         # Monta el directorio local de logs
    restart: always                              # Reinicia el contenedor si falla

```

### Iniciar los Servicios

```bash
docker-compose up -d
```

### Verificar el Estado del Contenedor

```bash
docker-compose ps
```

### Configuración con Sonarr y Radarr
Es necesario que la integración sea directamente a estos servicios. No funcionará con Prowlarr.
Se debe añadir un indexer de Torznab que apunte a la url ```https://ip:puerto```, siendo el puerto el añadido en el docker-compose.yml

## 🔧 Uso

- **Feeder en Segundo Plano:** El script `feeder.py` se ejecuta automáticamente como servicio.
- **Ejecución Periódica:** Los scripts `downloader.py` y `key_updater.py` se ejecutan cada 30 minutos para garantizar la actualización constante de los feeds RSS.

### Logs

Los logs se guardan en el directorio `./logs` en tu máquina host para su inspección.

## 📊 Arquitectura del Proyecto

```plaintext
.
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
├── src/
│   ├── downloader.py
│   ├── feeder.py
│   ├── key_updater.py
│   └── ...
├── logs/  # Directorio para guardar logs
├── rss.xml  # Archivo RSS de ejemplo
└── .env  # Variables de entorno
```

## 📢 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con mejoras o nuevas funcionalidades.

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más información.

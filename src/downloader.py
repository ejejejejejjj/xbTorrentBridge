import os
import requests
import zipfile

# Constantes con rutas absolutas
GITHUB_ZIP_URL = "https://raw.githubusercontent.com/ejejejejejjj/feed/main/feed.zip"  # Enlace del ZIP
ZIP_FILE = "/app/src/feed.zip"          # Ruta absoluta para el archivo ZIP descargado
EXTRACT_DIR = "/app"                    # Ruta absoluta para el directorio de extracción

def download_zip(url, output_path):
    """Descargar archivo ZIP desde GitHub."""
    print("[INFO] Descargando archivo ZIP desde GitHub...")
    response = requests.get(url)
    response.raise_for_status()
    with open(output_path, "wb") as file:
        file.write(response.content)
    print(f"[INFO] Archivo ZIP descargado: {output_path}")

def extract_zip(file_path, extract_to):
    """Extraer el contenido de un archivo ZIP."""
    print("[INFO] Extrayendo archivo ZIP...")
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"[INFO] Archivo ZIP extraído en: {extract_to}")

def run():
    try:
        # Descargar el ZIP
        download_zip(GITHUB_ZIP_URL, ZIP_FILE)
        # Extraer el contenido
        extract_zip(ZIP_FILE, EXTRACT_DIR)
        print("[INFO] Proceso de descarga y extracción completo.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        # Limpieza del archivo ZIP
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)

if __name__ == "__main__":
    run()

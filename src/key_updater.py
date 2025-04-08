import os
import xml.etree.ElementTree as ET

# Leer la clave RSS desde las variables de entorno
RSS_KEY = os.getenv("RSS_KEY")

if not RSS_KEY:
    raise ValueError("RSS_KEY no está definido en las variables de entorno")

# Ruta absoluta al archivo XML
XML_FILE = "/app/rss.xml"

# Cargar y procesar el archivo XML
def update_rss_key(xml_file, rss_key):
    """Actualizar los valores de guid, link y enclosure en el archivo XML."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Iterar sobre cada elemento <item>
    for item in root.findall(".//item"):
        # Actualizar el valor de <guid>
        guid = item.find("guid")
        if guid is not None and "REDACTED_RSS_KEY" in guid.text:
            guid.text = guid.text.replace("REDACTED_RSS_KEY", rss_key)
        
        # Actualizar el valor de <link>
        link = item.find("link")
        if link is not None and "REDACTED_RSS_KEY" in link.text:
            link.text = link.text.replace("REDACTED_RSS_KEY", rss_key)
        
        # Actualizar el valor del atributo url en <enclosure>
        enclosure = item.find("enclosure")
        if enclosure is not None and "REDACTED_RSS_KEY" in enclosure.attrib.get("url", ""):
            enclosure.set("url", enclosure.attrib["url"].replace("REDACTED_RSS_KEY", rss_key))
    
    # Guardar los cambios en el archivo XML
    tree.write(xml_file, encoding="UTF-8", xml_declaration=True)
    print(f"[INFO] Archivo {xml_file} actualizado correctamente.")

# Ejecutar el script
if __name__ == "__main__":
    update_rss_key(XML_FILE, RSS_KEY)

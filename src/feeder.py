from flask import Flask, request, Response
import xml.etree.ElementTree as ET
import re
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener puerto del archivo .env o usar el valor por defecto
PORT = int(os.getenv("PORT"))

# Ruta absoluta al archivo rss.xml
FILE_PATH = "/app/rss.xml"

app = Flask(__name__)

# Mapeo de nombres de temporadas a SXX
season_mapping = {
    "primera temporada": "S01",
    "segunda temporada": "S02",
    "tercera temporada": "S03",
    "cuarta temporada": "S04",
    "quinta temporada": "S05",
    "sexta temporada": "S06",
    "séptima temporada": "S07",
    "septima temporada": "S07",
    "octava temporada": "S08",
    "novena temporada": "S09",
    "décima temporada": "S10",
    "decima temporada": "S10"
}

# Lee el archivo RSS
def read_rss():
    with open(FILE_PATH, "r") as file:
        return file.read()

# Convierte nombres de temporada a formato SXX
def convert_season_to_sxx(title):
    for season_text, sxx in season_mapping.items():
        if season_text in title.lower():
            title = re.sub(
                rf"\b{season_text}\b", sxx, title, flags=re.IGNORECASE
            )
    return title

# Filtra por categorías
def filter_by_categories(item, categories, ns):
    if not categories:
        return True  # Si no se especifican categorías, pasa el filtro
    category_attr = item.find(".//ns0:attr[@name='category']", ns)
    if category_attr is not None:
        return category_attr.get("value") in categories
    return False

# Filtra por identificadores (imdbid, tmdbid, tvdbid)
def filter_by_identifiers(item, keys_and_values, ns):
    for key, value in keys_and_values:
        attr = item.find(f".//ns0:attr[@name='{key}']", ns)
        if attr is not None and attr.get("value") == value:
            return True
    return not keys_and_values  # Si no hay identificadores, pasa el filtro

# Filtra por temporada y episodio
def filter_by_season_episode(title, season=None, episode=None):
    if season:
        season_str = f"S{int(season):02}"
        if episode:
            episode_str = f"E{int(episode):02}"
            return re.search(rf"{season_str}\s*/?\s*{episode_str}", title, re.IGNORECASE)
        else:
            return re.search(rf"{season_str}", title, re.IGNORECASE) and not re.search(r"S\d{2}E\d{2}", title, re.IGNORECASE)
    return True  # Si no hay temporada, pasa el filtro

# Filtra por búsqueda en el título
def filter_by_query(title, query):
    if not query:
        return True

    # Extraer año del query si está presente
    match = re.search(r"(.*)\s+(\d{4})$", query)
    if match:
        base_query, year = match.groups()
        # Buscar el texto base y el año en el título
        return (base_query.lower() in title.lower() and year in title)
    else:
        # Buscar solo el texto base
        return query.lower() in title.lower()

# Filtra el feed completo
def filter_rss(rss_feed, categories=None, keys_and_values=None, season=None, episode=None, query=None):
    root = ET.fromstring(rss_feed)
    channel = root.find("channel")
    items = channel.findall("item")
    filtered_items = []

    # Namespace para los atributos
    ns = {'ns0': 'http://torznab.com/schemas/2015/feed'}

    for item in items:
        title = item.find("title").text
        title = convert_season_to_sxx(title)

        if (filter_by_categories(item, categories, ns) and
                filter_by_identifiers(item, keys_and_values, ns) and
                filter_by_season_episode(title, season, episode) and
                filter_by_query(title, query)):
            filtered_items.append(item)

    # Limpiar el canal y agregar los elementos filtrados
    for item in items:
        channel.remove(item)
    for item in filtered_items:
        channel.append(item)

    return ET.tostring(root, encoding="unicode")

@app.route("/api", methods=["GET"])
def torznab_feed():
    t = request.args.get("t", "")
    query = request.args.get("q", "")
    imdbid = request.args.get("imdbid", "")
    tmdbid = request.args.get("tmdbid", "")
    tvdbid = request.args.get("tvdbid", "")
    season = request.args.get("season", "")
    episode = request.args.get("ep", "")
    categories = request.args.get("cat", "").split(",") if request.args.get("cat") else None

    print(f"Request parameters: t={t}, q={query}, imdbid={imdbid}, "
          f"tmdbid={tmdbid}, tvdbid={tvdbid}, season={season}, ep={episode}, cat={categories}")

    if t == "caps":
        caps_xml = """<?xml version="1.0" encoding="UTF-8"?>
<caps>
  <server title="Torznab feed for Radarr/Sonarr (not Prowlarr)" />
  <limits default="100" max="100" />
  <searching>
    <search available="yes" supportedParams="q" />
    <tv-search available="yes" supportedParams="q,season,ep,imdbid,tvdbid,tmdbid" />
    <movie available="yes" supportedParams="q,imdbid,tmdbid" />
  </searching>
  <categories>
    <category id="2000" name="Movies" />
    <category id="3000" name="Audio" />
    <category id="5000" name="TV">
      <subcat id="5080" name="TV/Documentary" />
    </category>
    <category id="100004" name="Documentales" />
    <category id="100003" name="Música" />
    <category id="100001" name="Películas" />
    <category id="100002" name="Series" />
  </categories>
  <tags />
</caps>
"""
        return Response(caps_xml.strip(), mimetype="application/xml")

    elif t in ["search", "tvsearch", "movie"]:
        keys_and_values = []
        if imdbid:
            keys_and_values.append(("imdbid", imdbid))
        if tmdbid:
            keys_and_values.append(("tmdbid", tmdbid))
        if tvdbid:
            keys_and_values.append(("tvdbid", tvdbid))

        rss_feed = read_rss()
        filtered_feed = filter_rss(
            rss_feed,
            categories=categories,
            keys_and_values=keys_and_values,
            season=season,
            episode=episode,
            query=query
        )
        return Response(filtered_feed, mimetype="application/xml")

    else:
        return "Invalid request", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

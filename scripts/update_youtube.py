import os
import json
import requests
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

# Configuración desde variables de entorno (Secretos de GitHub)
API_KEY = os.environ.get('YOUTUBE_API_KEY')
# CHANNEL_ID = 'UC...' # Usaremos la variable, comentar si se usa hardcode
CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')

def fetch_videos():
    if not API_KEY or not CHANNEL_ID:
        print("Error: Faltan las variables de entorno YOUTUBE_API_KEY o YOUTUBE_CHANNEL_ID")
        return

    # Usamos 'search' para obtener los videos del canal
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=15"
    
    try:
        response = requests.get(url)
        # Check if response is not 200 OK before raising generic error
        if response.status_code != 200:
            print(f"Error API YouTube: {response.status_code}")
            print(response.text) # Imprimir el detalle del error JSON body
            response.raise_for_status()

        data = response.json()
        
        videos = []
        if 'items' in data:
            for item in data['items']:
                if item['id']['kind'] == "youtube#video":
                    # Extract high res thumbnail if available
                    thumbnails = item['snippet']['thumbnails']
                    # Prefer higher quality thumbnails
                    thumbnail_url = thumbnails.get('high', thumbnails.get('medium', thumbnails.get('default')))['url']
                    
                    video = {
                        'id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'publishedAt': item['snippet']['publishedAt'],
                        'thumbnail': thumbnail_url
                    }
                    videos.append(video)
        
        # Ensure directory exists
        os.makedirs('assets/data', exist_ok=True)
        
        # Save to JSON file (for frontend JS)
        with open('assets/data/videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
            print(f"Se han guardado {len(videos)} videos en assets/data/videos.json")

        # Generate Video Sitemap (for SEO)
        generate_video_sitemap(videos)

    except Exception as e:
        print(f"Error al obtener videos: {e}")
        exit(1)

def generate_video_sitemap(videos):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9", 
                        **{"xmlns:video": "http://www.google.com/schemas/sitemap-video/1.1"})
    
    # URL de la página donde se muestran los videos (la home)
    page_loc = "https://restorer.amorgante.es/"

    for video in videos:
        url_elem = ET.SubElement(urlset, "url")
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = page_loc

        unique_video = ET.SubElement(url_elem, "video:video")
        
        thumbnail_loc = ET.SubElement(unique_video, "video:thumbnail_loc")
        thumbnail_loc.text = video['thumbnail']
        
        title = ET.SubElement(unique_video, "video:title")
        title.text = video['title']
        
        description = ET.SubElement(unique_video, "video:description")
        # Google recomienda descripciones de hasta 2048 caracteres
        description.text = video['description'][:2048] if video['description'] else "Video de restauración de Home Auto Restorer"
        
        player_loc = ET.SubElement(unique_video, "video:player_loc")
        player_loc.text = f"https://www.youtube.com/embed/{video['id']}"
        
        publication_date = ET.SubElement(unique_video, "video:publication_date")
        # YouTube returns generic ISO string, sitemap expects W3C format (usually compatible)
        publication_date.text = video['publishedAt']

    # Prettify and save
    xmlstr = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="   ")
    
    # Save to root directory
    with open('sitemap-video.xml', 'w', encoding='utf-8') as f:
        f.write(xmlstr)
    print("Sitemap de videos generado en sitemap-video.xml")

if __name__ == "__main__":
    fetch_videos()

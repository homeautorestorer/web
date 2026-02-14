import os
import json
import requests

# Configuración desde variables de entorno (Secretos de GitHub)
API_KEY = os.environ.get('YOUTUBE_API_KEY')
# CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID') # Usaremos el ID directamente o lo pasaremos
CHANNEL_ID = 'UC...' # Placeholder, but better to use env var if it varies. Let's use env var.
CHANNEL_ID = os.environ.get('YOUTUBE_CHANNEL_ID')

def fetch_videos():
    if not API_KEY or not CHANNEL_ID:
        print("Error: Faltan las variables de entorno YOUTUBE_API_KEY o YOUTUBE_CHANNEL_ID")
        # For local testing without env vars, maybe fallback or exit
        return

    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=15"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        videos = []
        if 'items' in data:
            for item in data['items']:
                if item['id']['kind'] == "youtube#video":
                    # Extract high res thumbnail if available
                    thumbnails = item['snippet']['thumbnails']
                    thumbnail_url = thumbnails.get('medium', thumbnails.get('default'))['url']
                    
                    video = {
                        'id': item['id']['videoId'],
                        'title': item['snippet']['title'],
                        'thumbnail': thumbnail_url
                    }
                    videos.append(video)
        
        # Ensure directory exists
        os.makedirs('assets/data', exist_ok=True)
        
        # Save to JSON file
        with open('assets/data/videos.json', 'w', encoding='utf-8') as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)
            print(f"Se han guardado {len(videos)} videos en assets/data/videos.json")

    except Exception as e:
        print(f"Error al obtener videos: {e}")
        exit(1)

if __name__ == "__main__":
    fetch_videos()

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def get_latest_video(channel_id):
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "order": "date",
        "maxResults": 1,
        "type": "video",
        "key": API_KEY
    }
    res = requests.get(SEARCH_URL, params=params)
    data = res.json()
    items = data.get("items", [])
    if not items:
        return None
    video = items[0]
    return {
        "channel_id": channel_id,
        "channel_name": video["snippet"]["channelTitle"],
        "title": video["snippet"]["title"],
        "publishedAt": video["snippet"]["publishedAt"],
        "url": f"https://www.youtube.com/watch?v={video['id']['videoId']}"
    }

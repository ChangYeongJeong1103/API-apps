import os
import json
import re
from datetime import datetime
from youtube_api import get_latest_video
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


# === SETUP: Load configuration and history ===
# Read list of YouTube channel IDs to monitor
with open("channel_ids.txt", "r") as f:
    channel_ids = [line.strip() for line in f if line.strip()]

# Load previous video history to avoid processing same videos twice
if os.path.exists("history.json"):
    with open("history.json", "r") as f:
        history = json.load(f)
else:
    history = {}

# Storage for new videos found and their data
new_videos = []
video_scripts = {}

def extract_video_id(url):
    """Extract video ID from YouTube URL (e.g., 'dQw4w9WgXcQ' from full URL)"""
    match = re.search(r"v=([\w-]+)", url)
    return match.group(1) if match else None

def get_transcript(video_url):
    """
    Fetch transcript from YouTube video
    Args:
        video_url: Full YouTube URL (e.g., "https://www.youtube.com/watch?v=...")
    Returns:
        String containing the transcript text, or error message if failed
    """
    video_id = extract_video_id(video_url)
    try:
        # Try to get transcript in Korean first, then English
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["ko", "en"])
        # Join all transcript entries into one string
        return " ".join([entry["text"] for entry in transcript_list])
    except (TranscriptsDisabled, NoTranscriptFound) as e:
        return f"[Transcript Error: {str(e)}]"
    except Exception as e:
        return f"[Transcript Error: {str(e)}]"

# === MAIN PROCESSING: Check each channel for new videos ===
for channel_id in channel_ids:
    # Get the latest video from this channel
    video = get_latest_video(channel_id)
    if not video:
        continue
        
    video_url = video["url"]
    video_id = extract_video_id(video_url)

    # Check if this is a new video (not in our history)
    if channel_id not in history or history[channel_id] != video_id:
        history[channel_id] = video_id

        # Get transcript from YouTube
        transcript = get_transcript(video_url)

        new_videos.append({
            "timestamp": datetime.now().isoformat(),
            "url": video_url,
            "title": video["title"],
            "channel_id": channel_id,
            "channel_name": video["channel_name"]
        })

        video_scripts[channel_id] = {
            "date": datetime.now().strftime("%-m/%-d/%y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "title": video["title"],
            "url": video_url,
            "transcript": transcript,
            "channel_name": video["channel_name"]
        }

        # Save individual transcript file for easy copy-paste
        # Clean channel name and video title for filename
        safe_channel_name = re.sub(r'[<>:"/\\|?*]', '_', video["channel_name"])
        # Remove parentheses part from title (often redundant channel name)
        title_without_parentheses = re.sub(r'\s*\([^)]*\)\s*$', '', video["title"])
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title_without_parentheses)
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"transcripts/{date_str}_{safe_channel_name}_{safe_title}.txt"
        
        # Create transcripts directory if not exists
        os.makedirs("transcripts", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Title: {video['title']}\n")
            f.write(f"Channel ID: {channel_id}\n") 
            f.write(f"URL: {video_url}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("-" * 50 + "\n\n")
            f.write("TRANSCRIPT:\n")
            f.write(transcript)
            f.write("\n\n" + "="*50 + "\n")
            f.write("- Summarize the above financial and investment-related article into exactly 10 concise bullet points.\n")
            f.write("- Each point should highlight key facts, trends, or implications related to stocks, markets, or companies mentioned in the article.\n")
            f.write("- Use clear, professional language suitable for investors. Include relevant numbers (e.g., % changes, EPS, revenue) shown in the article.\n")
            f.write("- Avoid repetition. Maintain chronological or logical order.\n")
            

        print(f"✅ New video detected: {video['title']}")
        print(f"📺 Channel: {video['channel_name']}")
        print(f"📄 Transcript saved: {filename}")
        
        
# === SAVE RESULTS: Update history and generate output files ===
# Save updated history to avoid reprocessing same videos
with open("history.json", "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

# Save video data in JSON format for other scripts to use
with open("video_scripts.json", "w", encoding="utf-8") as f:
    json.dump(video_scripts, f, indent=2, ensure_ascii=False)

# Save HTML output file
with open("new_videos.html", "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
    f.write("<meta charset='UTF-8'>\n<title>New YouTube Videos</title>\n")
    f.write("<style>body{font-family:Arial;margin:20px;} a{color:#1976d2;}</style>\n")
    f.write("</head>\n<body>\n<h1>New YouTube Videos</h1>\n")
    
    if new_videos:
        for video in new_videos:
            f.write(f"<div style='margin-bottom:15px;'>\n")
            f.write(f"<p><strong>[{video['timestamp']}]</strong></p>\n")
            f.write(f"<p>📺 <a href='{video['url']}' target='_blank'>{video['title']}</a></p>\n")
            f.write(f"<p>📺 Channel: {video['channel_name']}</p>\n")
            f.write("</div>\n")
    else:
        f.write("<p>No new videos found.</p>\n")
    
    f.write("</body>\n</html>")

# Save text output file
with open("new_videos.txt", "w", encoding="utf-8") as f:
    f.write(f"=== New YouTube Videos Notification ===\n")
    f.write(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    if new_videos:
        for video in new_videos:
            f.write(f"[{video['timestamp']}]\n")
            f.write(f"Title: {video['title']}\n")
            f.write(f"Link: {video['url']}\n")
            f.write(f"Channel: {video['channel_name']}\n")
            f.write(f"Channel ID: {video['channel_id']}\n")
            f.write("-" * 50 + "\n")
    else:
        f.write("No new videos found.\n")

print(f"\n📊 Summary:")
print(f"- Checked {len(channel_ids)} channels")
print(f"- Found {len(new_videos)} new videos")
print(f"- Results saved in 'new_videos.html' and 'new_videos.txt'")
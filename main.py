import os
import feedparser
import requests
import time

# 🔹 Read secrets from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in Railway secrets
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Set this in Railway secrets
RSS_URL = os.getenv("RSS_URL")  # Set this in Railway secrets

# Track the last posted video
last_video_id = None

def get_latest_video():
    """Fetch the latest video from the YouTube RSS feed."""
    feed = feedparser.parse(RSS_URL)
    latest_video = feed.entries[0]
    video_id = latest_video.yt_videoid
    video_title = latest_video.title
    video_url = latest_video.link
    return video_id, video_title, video_url

def send_to_telegram(video_title, video_url):
    """Send the new video announcement to the Telegram channel."""
    message = f"📢 *New Video Alert!*\n🎥 *{video_title}*\n🔗 [Watch here]({video_url})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, params=params)
    return response.json()

while True:
    try:
        video_id, video_title, video_url = get_latest_video()
        
        if video_id != last_video_id:  # Check if it's a new video
            send_to_telegram(video_title, video_url)
            last_video_id = video_id  # Update last posted video
        
        time.sleep(600)  # Check every 10 minutes
    except Exception as e:
        print("Error:", e)
        time.sleep(60)  # Wait 1 minute before retrying

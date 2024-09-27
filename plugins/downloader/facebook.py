import requests
import os
from telebot import types

def download_facebook_video(url):
    api_url = f"https://api.ryzendesu.vip/api/downloader/fbdl?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["status"]:
            video_data = data["data"]
            for video in video_data:
                if video["resolution"] == "720p (HD)":
                    video_url = video["url"]
                    break
            else:
                return None
            return video_url
        else:
            return None
    else:
        return None

def fb_handler(message, bot):
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a Facebook video URL.")
        return

    url = message.text.split()[1]
    if url.startswith('https://www.facebook.com/'):
        video_url = download_facebook_video(url)
        if video_url is not None:
            bot.reply_to(message, "Downloading video...")
            video_response = requests.get(video_url, stream=True)
            if video_response.status_code == 200:
                video_file_name = f"fb_video.mp4"
                with open(video_file_name, "wb") as f:
                    for chunk in video_response.iter_content(1024):
                        f.write(chunk)
                bot.send_video(message.chat.id, open(video_file_name, 'rb'), caption="•───────────────────•\n© Leneath™ | 2024")
                os.remove(video_file_name)
            else:
                bot.reply_to(message, f"Failed to download video: {video_url}")
        else:
            bot.reply_to(message, "Failed to retrieve video data")
    else:
        bot.reply_to(message, "Invalid Facebook video URL. Please try again.")
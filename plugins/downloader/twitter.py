import requests
import os
from telebot import types

def download_twitter_video(message, bot):
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a Twitter / X video URL.")
        return

    url = message.text.split()[1]
    if url.startswith('https://twitter.com/') or url.startswith('https://x.com/'):
        api_url = f"https://api.ryzendesu.vip/api/downloader/twitter?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                media_data = data["media"][0]
                video_url = media_data["url"]
                bot.reply_to(message, "Downloading video...")
                video_response = requests.get(video_url, stream=True)
                if video_response.status_code == 200:
                    video_file_name = f"twitter_video.mp4"
                    with open(video_file_name, "wb") as f:
                        for chunk in video_response.iter_content(1024):
                            f.write(chunk)
                    bot.send_video(message.chat.id, open(video_file_name, 'rb'), caption="•───────────────────•\n© Leneath™ | 2024")
                    os.remove(video_file_name)
                else:
                    bot.reply_to(message, f"Failed to download video: {video_url}")
            else:
                bot.reply_to(message, f"Failed to retrieve video data: {data['msg']}")
        else:
            bot.reply_to(message, f"Failed to connect to API: {response.status_code}")
    else:
        bot.reply_to(message, "Invalid Twitter video URL. Please try again.")
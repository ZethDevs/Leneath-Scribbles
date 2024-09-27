import requests
import os
from telebot import types

def download_instagram_video(message, bot):
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a Instagram video URL.")
        return

    url = message.text.split()[1]
    if url.startswith('https://www.instagram.com/'):
        api_url = f"https://api.ryzendesu.vip/api/downloader/igdl?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                video_data = data["data"][0]
                video_url = video_data["url"]
                thumbnail_url = video_data["thumbnail"]
                bot.reply_to(message, "Downloading video...")
                video_response = requests.get(video_url, stream=True)
                if video_response.status_code == 200:
                    video_file_name = f"ig_video.mp4"
                    with open(video_file_name, "wb") as f:
                        for chunk in video_response.iter_content(1024):
                            f.write(chunk)
                    thumbnail_response = requests.get(thumbnail_url)
                    if thumbnail_response.status_code == 200:
                        thumbnail_file_name = f"ig_thumbnail.jpg"
                        with open(thumbnail_file_name, "wb") as f:
                            f.write(thumbnail_response.content)
                        bot.send_video(message.chat.id, open(video_file_name, 'rb'), caption="•───────────────────•\n© Leneath™ | 2024", duration=None, thumb=open(thumbnail_file_name, 'rb'))
                        os.remove(video_file_name)
                        os.remove(thumbnail_file_name)
                    else:
                        bot.reply_to(message, f"Failed to download thumbnail: {thumbnail_url}")
                else:
                    bot.reply_to(message, f"Failed to download video: {video_url}")
            else:
                bot.reply_to(message, f"Failed to retrieve video data: {data['msg']}")
        else:
            bot.reply_to(message, f"Failed to connect to API: {response.status_code}")
    else:
        bot.reply_to(message, "Invalid Instagram video URL. Please try again.")
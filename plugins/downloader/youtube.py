import requests
import os
from telebot import types

def download_youtube_video(message, bot):
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a YouTube video URL.")
        return

    url = message.text.split()[1]
    if url.startswith('https://www.youtube.com/'):
        api_url = f"https://api.nyxs.pw/dl/yt-direct?url={url}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            if data["status"]:
                video_data = data["result"]
                video_url = video_data["urlVideo"]
                title = video_data["title"]
                deskripsi = video_data["description"]
                thumbnail_url = video_data["thumbnail"]
                urlAudio = video_data["urlAudio"]
                channel = video_data["channelName"]
                markup = types.InlineKeyboardMarkup()
                btn_video = types.InlineKeyboardButton('Video HD', url=video_url)
                btn_audio = types.InlineKeyboardButton('Audio Only', url=urlAudio)
                markup.add(btn_video, btn_audio)
                
                bot.send_message(message.chat.id, f"==========[ Description ]==========\n{deskripsi}\n=============================\n🌐 Channel : {channel}\n📁 Title : {title}\n•───────────────────•\n© Leneath™ | 2024", reply_markup=markup)
            else:
                bot.reply_to(message, f"Failed to retrieve video data: {data['msg']}")
        else:
            bot.reply_to(message, f"Failed to connect to API: {response.status_code}")
    else:
        bot.reply_to(message, "Invalid YouTube video URL. Please try again.")
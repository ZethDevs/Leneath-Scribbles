import requests
import os
from telebot import types

def download_spotify(message, bot):
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a Spotify video URL.")
        return

    url = message.text.split()[1]
    if not url.startswith('https://open.spotify.com/'):
        bot.reply_to(message, 'Invalid Spotify URL. Please use the format https://open.spotify.com/...')
        return
    api_url = f'https://api.nyxs.pw/dl/spotify?url={url}'
    response = requests.get(api_url)
    data = response.json()
    if data['status']:
        music_url = data['result']['url']
        bot.reply_to(message, f'Downloading Music...')
        audio_response = requests.get(music_url, stream=True)
        if audio_response.status_code == 200:
            bot.send_audio(message.chat.id, audio_response.content)
        else:
            bot.reply_to(message, 'Failed to download music.')
    else:
        bot.reply_to(message, 'Failed to download music.')
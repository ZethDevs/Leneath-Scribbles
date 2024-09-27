import telebot
import requests
import re
from datetime import datetime
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
import types
from plugins.ai import gpt4, gpt4o, gemini, cai, cai2
from plugins.downloader import tiktok, facebook, instagram, twitter, youtube, spotify
from plugins.other import lookup

bot_token = "7245725446:AAGVINnM5nO48c-Say95k2wZYu23Lvs70Mk"

bot = telebot.TeleBot(bot_token)

ADMIN_ID = 1951554771

btn1 = InlineKeyboardButton('♥️ Developer', url='https://t.me/leneath')
btn2 = InlineKeyboardButton('💎 Donate', url='https://t.me/leneath')
ch = InlineKeyboardButton('🌐 Channel', url='https://t.me/LeneathCH')

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id  # Mendapatkan ID pengguna
    first = message.from_user.first_name
    last = message.from_user.last_name
    user = message.from_user.username
    gg = message.from_user.id
    b = InlineKeyboardMarkup()
    b.add(btn1, btn2)
    b.add(ch)
    
    # Membuat atau membaca file user.txt
    file_path = "user.txt"
    user_exists = False
    
    # Cek apakah file user.txt ada
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if f"ID : {user_id}" in line:
                    user_exists = True
                    break
    
    # Jika pengguna sudah terdaftar, tidak menyimpan lagi
    if not user_exists and not str(user_id).startswith('-100'):
        with open(file_path, "a") as file:
            file.write(f"====================\nID : {user_id}\nName : {first}\nUsername : @{user}\n")
    
    now = datetime.now()
    
    # Format the date and time
    runtime = now.strftime("%H Hour, %M Minute, %S Seconds")
    hari = now.strftime("%A")
    tanggal = now.strftime("%m/%d/%Y")
    
    try:
        with open("user.txt", "r") as f:
            user_list = f.readlines()
            # Counting the number of lines that contain "ID :"
            user_count = sum(1 for line in user_list if line.startswith("ID :"))
            bot.send_photo(
                message.chat.id,
                "https://telegra.ph/file/2ad518679273ed8e92244.jpg",
                f"""┌─────────────────────┈ ⳹\n│ ❐ Developer : @Leneath\n│ ❐ Total User : {user_count}\n│ ❐ Runtime : {runtime}\n│ ❐ Day : {hari}\n│ ❐ Date : {tanggal}\n└─────────────────────┈ ⳹\n┌──── 「 𝗗𝗘𝗩 」\n│ ❐ /broadcast - Message to user\n│ ❐ /restart - Restart Bot\n│ ❐ /shutdown - Shutdown Bot\n└─────────────────────┈ ⳹\n┌──── 「 𝗔𝗜 」\n│ ❐ /gpt4o - GPT-4o\n│ ❐ /gpt4 - GPT-4\n│ ❐ /gemini - Gemini AI\n│ ❐ /cai - Leneath (Tsundere)\n│ ❐ /cai2 - Leneath (Dandere)\n└─────────────────────┈ ⳹\n┌──── 「 𝗗𝗢𝗪𝗡𝗟𝗢𝗔𝗗𝗘𝗥 」\n│ ❐ /tiktok - Tiktok\n│ ❐ /facebook - Facebook\n│ ❐ /instagram - Instagram\n│ ❐ /twitter or /x - Twitter / X\n│ ❐ /youtube - YouTube\n│ ❐ /spotify - Spotify\n└─────────────────────┈ ⳹\n┌──── 「 𝗢𝗧𝗛𝗘𝗥 」\n│ ❐ /lookup - domain/ip\n└─────────────────────┈ ⳹\n© 2024 𝖠𝗅𝗅 𝗋𝗂𝗀𝗁𝗍 𝗋𝖾𝗌𝖾𝗋𝗏𝖾𝖽 | Leneath""", 
                reply_markup=b
            )
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id == ADMIN_ID:
        try:
            if len(message.text.split()) > 1:
                broadcast_text = message.text[11:]
                with open("user.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.startswith("ID : "):
                            user_id = int(line.strip().split(": ")[1])
                            try:
                                bot.send_message(user_id, broadcast_text)
                                bot.reply_to(message, f"Message sent to user {user_id}.")
                            except Exception as e:
                                bot.reply_to(message, f"Error sending message to user {user_id}: {e}")
            else:
                bot.reply_to(message, "Please provide a message to broadcast after the /broadcast command.")
        except FileNotFoundError:
            bot.reply_to(message, "File user.txt not found.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
    else:
        bot.reply_to(message, "You are not authorized to use this command!")

@bot.message_handler(commands=['restart'])
def start_handler(message):
    bot.reply_to(message, "You are not authorized to use this command!")
    
@bot.message_handler(commands=['shutdown'])
def start_handler(message):
    bot.reply_to(message, "You are not authorized to use this command!")

#================== [ AI TOOLS ] ================================
@bot.message_handler(commands=['gpt4'])
def gpt4_command(message):
    gpt4.gpt4_handler(message, bot)
           
@bot.message_handler(commands=['gpt4o'])
def gpt4o_command(message):
    gpt4o.gpt4o_handler(message, bot)
    
@bot.message_handler(commands=['gemini'])
def gemini_command(message):
    gemini.gemini_handler(message, bot)
    
@bot.message_handler(commands=['cai'])
def cai_command(message):
    cai.cai_handler(message, bot)
    
@bot.message_handler(commands=['cai2'])
def cai2_command(message):
    cai2.cai2_handler(message, bot)
#================== [ Downloader TOOLS ] ================================
@bot.message_handler(commands=['tiktok'])
def tt_command(message):
    tiktok.tt_handler(message, bot)

@bot.message_handler(commands=['facebook'])
def fb_command(message):
    facebook.fb_handler(message, bot)

@bot.message_handler(commands=['instagram'])
def download_instagram_video_command(message):
    instagram.download_instagram_video(message, bot)

@bot.message_handler(commands=["twitter", "x"])
def download_twitter_video_command(message):
    twitter.download_twitter_video(message, bot)

@bot.message_handler(commands=['youtube'])
def download_youtube_video_command(message):
    youtube.download_youtube_video(message, bot)

@bot.message_handler(commands=['spotify'])
def download_spotify_music_command(message):
    spotify.download_spotify(message, bot)
#==========================[ 𝗢𝗧𝗛𝗘𝗥 ] ==================================
@bot.message_handler(commands=['lookup'])
def lookup_command(message):
    lookup.handle_domain(message, bot)

if __name__ == "__main__":
    from web import keep_alive
    keep_alive()
    bot.infinity_polling()
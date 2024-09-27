import requests
import re
from telebot import types

def get_cai_response(prompt):
    url = f"https://api.nyxs.pw/ai/character-ai?prompt={prompt}&gaya=reply as Leneath tsundere girlfriend"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data["result"]
        if result is not None:
            result = re.sub(r'([_{}\[\]()~>#+\-=|\.!])', r'\\\1', result)
            return result
        else:
            return "Error: Unable to retrieve response"
    else:
        return f"Error: Unable to connect to API ({response.status_code})"

def cai_handler(message, bot):
    if len(message.text) == 4:  # hanya /cai, tidak ada prompt
        bot.reply_to(message, "Example: /cai i love you")
    else:
        prompt = message.text[5:]  # remove the /cai command
        response = get_cai_response(prompt)
        bot.reply_to(message, response, parse_mode="MarkdownV2")
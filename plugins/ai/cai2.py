import requests
import re
from telebot import types

def get_cai2_response(prompt):
    url = f"https://api.nyxs.pw/ai/character-ai?prompt={prompt}&gaya=reply as Leneath dandere girlfriend"
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

def cai2_handler(message, bot):
    if len(message.text) == 5:  # hanya /cai2, tidak ada prompt
        bot.reply_to(message, "Example: /cai2 i love you")
    else:
        prompt = message.text[6:]  # remove the /cai2 command
        response = get_cai2_response(prompt)
        bot.reply_to(message, response, parse_mode="MarkdownV2")
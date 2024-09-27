import requests
import re
from telebot import types

def get_gemini_response(prompt):
    url = f"https://api.nyxs.pw/ai/gemini-advance?text={prompt}"
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

def gemini_handler(message, bot):
    if len(message.text) == 7:  # hanya /gemini, tidak ada prompt
        bot.reply_to(message, "Example: /gemini hello")
    else:
        prompt = message.text[8:]  # remove the /gemini command
        response = get_gemini_response(prompt)
        bot.reply_to(message, response, parse_mode="MarkdownV2")
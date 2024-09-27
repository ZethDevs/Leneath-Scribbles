import requests
import re
from telebot import types

def get_gpt4_response(prompt):
    url = f"https://api.nyxs.pw/ai/gpt4?text={prompt}"
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

def gpt4_handler(message, bot):
    if len(message.text) == 5:  # hanya /gpt4, tidak ada prompt
        bot.reply_to(message, "Example: /gpt4 hello")
    else:
        prompt = message.text[6:]  # remove the /gpt4 command
        response = get_gpt4_response(prompt)
        bot.reply_to(message, response, parse_mode="MarkdownV2"

import requests
import re
from telebot import types

def get_gpt4o_response(prompt):
    url = f"https://api.nyxs.pw/ai/gpt4o?text={prompt}&system=reply as AI know everything"
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

def gpt4o_handler(message, bot):
    if len(message.text) == 6:  # hanya /gpt4o, tidak ada prompt
        bot.reply_to(message, "Example: /gpt4o hello")
    else:
        prompt = message.text[7:]  # remove the /gpt4o command
        response = get_gpt4o_response(prompt)
        bot.reply_to(message, response, parse_mode="MarkdownV2")
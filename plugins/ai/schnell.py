import telebot
import requests
from retrying import retry

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_api_response(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response

def schnell_handler(message, bot):
    if message.text.startswith('/schnell'):
      if message.text == '/schnell':
        bot.send_message(message.chat.id, 'Example : /schnell girl with bikini holding ice cream')
    else:
        prompt = message.text[9:]  # Remove the /schnell command
        api_url = f'https://api.ryzendesu.vip/api/ai/flux-schnell?prompt={prompt}'
        try:
            response = get_api_response(api_url)
            with open('image.jpeg', 'wb') as f:
                f.write(response.content)
            with open('image.jpeg', 'rb') as f:
                bot.send_photo(message.chat.id, f)
            import os
            os.remove('image.jpeg')  # Remove the temporary image file
        except requests.exceptions.RequestException as e:
            bot.send_message(message.chat.id, 'Failed to generate image')
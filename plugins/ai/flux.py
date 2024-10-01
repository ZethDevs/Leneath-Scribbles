import telebot
import requests
from retrying import retry

@retry(wait_exponential_multiplier=1000, wait_exponential_max=10000)
def get_api_response(api_url):
    response = requests.get(api_url)
    response.raise_for_status()
    return response

def flux_diffusion_handler(message, bot):
    if message.text.startswith('/flux'):
        if message.text == '/flux':
            bot.send_message(message.chat.id, 'Example : /flux girl with bikini holding ice cream')
        else:
            prompt = message.text[6:]  # Remove the /flux command
            if prompt:  # Check if the user provided a prompt
                bot.send_message(message.chat.id, 'Generate images...')
                api_url = f'https://api.ryzendesu.vip/api/ai/flux-diffusion?prompt={prompt}'
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
            else:
                bot.send_message(message.chat.id, 'example : /flux a girl with uniform school pink hair')
import telebot
import requests

def photoleap_handler(message, bot):
    if message.text == '/photoleap':
        bot.send_message(message.chat.id, 'Example : /photoleap girl with bikini holding ice cream')
        bot.register_next_step_handler(message, lambda msg: generate_image(bot, msg))
    else:
        prompt = message.text.replace('/photoleap ', '')
        generate_image(bot, message, prompt)

def generate_image(bot, message, prompt=None):
    if prompt is None:
        prompt = message.text
    api_url = f'https://deku-rest-api.gleeze.com/aigen?prompt={prompt}'
    response = requests.get(api_url)
    data = response.json()
    image_url = data['result']
    bot.send_message(message.chat.id, 'Generating image...')
    bot.send_photo(message.chat.id, image_url)
    bot.send_message(message.chat.id, 'Image generated!')
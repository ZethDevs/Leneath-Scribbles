import requests
import random
import urllib.parse
import re
from telebot import TeleBot, types
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def valid(url):
    regex = r'^(https?://(www\.)?terabox\.com/(s|wap/share))'
    return bool(re.match(regex, url))

def fetch(url):
    if not valid(url):
        raise ValueError('Invalid Link, Example "https://terabox.com/s/" atau "https://www.terabox.com/wap/share".')

    url_api = 'https://testterabox.vercel.app/api'
    headers = {
        'authority': 'testterabox.vercel.app',
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'Postify/1.0.0',
        'x-forwarded-for': '.'.join(str(random.randint(0, 255)) for _ in range(4))
    }

    body = {'url': url}
    try:
        response = requests.post(url_api, json=body, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f'Error: {e.response.status_code if e.response else e}')

    proxy = "https://teraboxdownloader.online/proxy.php?url="
    data = response.json()
    for key in ['link', 'direct_link']:
        if key in data:
            data[key] = proxy + urllib.parse.quote(data[key])

    return data

def terabox_command(message, bot):
    try:
        url = message.text.split()[1]
        data = fetch(url)
        direct_link = data.get('direct_link')

        # Buat adapter dengan retry mechanism
        adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1))
        session = requests.Session()
        session.mount('https://', adapter)

        # Download file dengan timeout
        response = session.get(direct_link, stream=True, timeout=30)

        # Tentukan jenis file
        file_type = response.headers.get('Content-Type')
        if file_type.startswith('video/'):
            # Kirim video
            bot.send_video(message.chat.id, response.content, caption='© Leneath™ | 2024')
        elif file_type.startswith('image/'):
            # Kirim foto
            bot.send_photo(message.chat.id, response.content, caption='© Leneath™ | 2024')
        else:
            # Kirim dokumen
            bot.send_document(message.chat.id, response.content, caption='© Leneath™ | 2024')
    except ValueError as e:
        bot.send_message(message.chat.id, f'Error: {e}')
    except IndexError:
        bot.send_message(message.chat.id, 'Usage: /terabox <TeraBox link>')
import requests
import re
from telebot import types
import os
import json
import sys
import validators
from bs4 import BeautifulSoup

def api(ip_address):
    try:
        # Validasi input
        if not validators.ipv4(ip_address) and not validators.domain(ip_address):
            return f"{ip_address} is not a valid IP address or domain."

        url = "https://iplookup.chrishsec.com/"
        headers = {
            "Host": "iplookup.chrishsec.com",
            "User-Agent": "IPlookup/v1.0.0",
            "Authorization": "Bearer 3ca64848-8bce-41a3-9dbb-3fecf583b85e",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://iplookup.chrishsec.com",
            "Referer": "https://iplookup.chrishsec.com/",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Dnt": "1",
            "Sec-Gpc": "1",
            "Te": "trailers",
        }

        data = {
            "ipAddress": ip_address
        }

        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')

        json_data = None
        for script_tag in script_tags:
            script_text = script_tag.get_text()
            if 'var jsonData =' in script_text:
                json_data = re.search(r'var jsonData = (.+?);', script_text).group(1)
                decoded_info = json.loads(json_data)

                output = "•══════════•●•══════════•\n"
                output += print_info(decoded_info, 'ipaddress', 'IP Address')
                output += print_info(decoded_info, 'country', 'Country')
                output += print_info(decoded_info, 'countrycode', 'Country Code')
                output += print_info(decoded_info, 'city', 'City')
                output += print_info(decoded_info, 'zip', 'Zip Code')
                output += print_info(decoded_info, 'lat', 'Latitude')   
                output += print_info(decoded_info, 'lon', 'Longitude')
                output += print_info(decoded_info, 'timezone', 'Time zone')
                output += print_info(decoded_info, 'isp', 'ISP')
                output += print_info(decoded_info, 'org', 'ORG')
                output += print_info(decoded_info, 'asn', 'ASN')
                output += "•═══════════════════════•"
                return output
    except requests.exceptions.RequestException as e:
        return f"Error while accessing API: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON: {e}"
    except AttributeError as e:
        return f"Error while retrieving data from JSON: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

def print_info(data, key, label):
    value = data.get(key, 'N/A') if key in data and data[key] else 'N/A'
    return f"*◉ {label} :* `{value}`\n"
    
def handle_domain(message, bot):
    # Periksa apakah ada argumen setelah perintah /domain
    if len(message.text.split()) > 1:
        ip_address = message.text.split()[1]
        result = api(ip_address)
        bot.reply_to(message, result, parse_mode="Markdown")
    else:
        bot.reply_to(message, "example :\n/lookup www.google.com\n/lookup 104.22.5.240")
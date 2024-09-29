import telebot
import requests

def subdomain_handler(message, bot):
    if len(message.text.split()) == 1:
        bot.reply_to(message, "Please provide a domain name. Example: /subdomain viu.com")
    else:
        domain = message.text.split()[1]
        api_url = f"https://api.agatz.xyz/api/subdomain?url={domain}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            subdomains = data['data']
            subdomains = list(set(subdomains))  # remove duplicates
            subdomains_str = '\n'.join(subdomains)
            bot.reply_to(message, f"Subdomains for {domain} :\n{subdomains_str}")
        else:
            bot.reply_to(message, "Error: Unable to retrieve subdomains try again.")
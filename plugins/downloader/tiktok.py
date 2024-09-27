import requests
import os
from telebot import types

def download_tiktok_video(url):
    api_url = f"https://api.ryzendesu.vip/api/downloader/ttdl?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["code"] == 0:
            video_data = data["data"]
            video_title = video_data["title"]
            video_id = video_data["id"]
            hd_play_url = video_data["hdplay"]
            thumbnail_url = video_data["cover"]
            duration = video_data["duration"]
            size = video_data["hd_size"]
            region = video_data["region"]
            return {
                "video_title": video_title,
                "video_id": video_id,
                "hd_play_url": hd_play_url,
                "thumbnail_url": thumbnail_url,
                "duration": duration,
                "size": size,
                "region": region
            }
        else:
            return None
    else:
        return None

def tt_handler(message, bot):
    print(f"Received message: {message.text}")
    if len(message.text.split()) == 1:  # Check if no link is provided
        bot.reply_to(message, "Please provide a Tiktok video URL.")
        return

    url = message.text.split()[1]
    print(f"Extracted URL: {url}")
    if url.startswith('https://vt.tiktok.com/') or url.startswith('https://vm.tiktok.com/'):
        print("Valid TikTok URL detected")
        video_data = download_tiktok_video(url)
        if video_data is not None:
            print("Video data retrieved successfully")
            video_title = video_data["video_title"]
            video_id = video_data["video_id"]
            hd_play_url = video_data["hd_play_url"]
            thumbnail_url = video_data["thumbnail_url"]
            duration = video_data["duration"]
            size = video_data["size"]
            region = video_data["region"]
            bot.reply_to(message, "Downloading video...")
            video_response = requests.get(hd_play_url, stream=True)
            if video_response.status_code == 200:
                video_file_name = f"{video_id}.mp4"
                with open(video_file_name, "wb") as f:
                    for chunk in video_response.iter_content(1024):
                        f.write(chunk)
                thumbnail_response = requests.get(thumbnail_url)
                if thumbnail_response.status_code == 200:
                    thumbnail_file_name = f"{video_id}.jpg"
                    with open(thumbnail_file_name, "wb") as f:
                        f.write(thumbnail_response.content)
                    bot.send_video(message.chat.id, open(video_file_name, 'rb'), caption=f"==========[ Caption ]==========\n{video_title}\n=============================\n🌐 Region : {region}\n📁 Size : {size}\n⏳ Duration : {duration}\n•───────────────────•\n© Leneath™ | 2024", duration=duration, thumb=open(thumbnail_file_name, 'rb'))
                    os.remove(video_file_name)
                    os.remove(thumbnail_file_name)
                else:
                    bot.reply_to(message, f"Failed to download thumbnail: {thumbnail_url}")
            else:
                bot.reply_to(message, f"Failed to download video: {video_title} ({video_id})")
        else:
            bot.reply_to(message, "Failed to retrieve video data")
    else:
        bot.reply_to(message, "Invalid TikTok video URL. Please try again.")
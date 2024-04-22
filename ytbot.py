import io
import os
import telebot
import yt_dlp
from telebot import types

API_TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Просто отправь мне ссылку на видео с YouTube, и я скачаю его для тебя!")

@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_message(message):
    if 'youtube.com' in message.text or 'youtu.be' in message.text:
        download_video(message)
    else:
        bot.reply_to(message, "Пожалуйста, отправь ссылку на видео с YouTube.")

def download_video(message):
    url = message.text.strip()
    with yt_dlp.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'format': 'best'}) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get('id', None)
        video_ext = info_dict.get('ext', 'mp4')
        video_file = f'{video_id}.{video_ext}'
        bot.send_video(message.chat.id, open(video_file, 'rb'))
        os.remove(video_file)

bot.infinity_polling()
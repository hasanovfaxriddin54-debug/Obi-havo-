import os
import requests
from flask import Flask
from telebot import TeleBot
from threading import Thread

# 1. SOZLAMALAR
BOT_TOKEN = "8214592685:AAHSk7369j8Pf4QlP4VTO fzrJC7Yqv-RfaQ"
WEATHER_API_KEY = "80998394e1011867c4e4eb789c656910"
bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ishlayapti! ✅"

# 2. OB-HAVO FUNKSIYASI
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=uz"
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            return f"🌤 {city.capitalize()}da ob-havo:\n🌡 Harorat: {temp}°C\n☁️ Holat: {desc}"
        else:
            return "❌ Shahar topilmadi. Iltimos, nomini inglizcha yozing (masalan: Tashkent)."
    except:
        return "⚠️ Xatolik yuz berdi."

# 3. TELEGRAM XABARLARINI QABUL QILISH
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Ob-havoni bilish uchun shahar nomini yozing.")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    city = message.text
    result = get_weather(city)
    bot.reply_to(message, result)

# 4. SERVERNI YURGIZISH
def run():
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.polling(none_stop=True)
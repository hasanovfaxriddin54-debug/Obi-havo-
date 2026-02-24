import os
import requests
from flask import Flask
from telebot import TeleBot
from threading import Thread

# 1. SOZLAMALAR
BOT_TOKEN = "8214592685:AAHSk7369j8Pf4QlP4VTOfzrJC7Yqv-RfaQ"
WEATHER_API_KEY = "80998394e1011867c4e4eb789c656910" # Bu tekin kalit
bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

# 2. RENDER UCHUN SERVER
@app.route('/')
def home():
    return "Ob-havo boti yoniq! ✅"

# 3. OB-HAVO FUNKSIYASI
def get_weather(city):
   response = requests.get(url)
        data = response.json()
        
        # Agar shahar topilsa (kod 200 bo'lsa)
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            
            answer = (f"🌤 {city.capitalize()} shahridagi ob-havo:\n\n"
                      f"🌡 Harorat: {temp}°C\n"
                      f"☁️ Holat: {desc}\n"
                      f"💧 Namlik: {humidity}%\n"
                      f"💨 Shamol: {wind} m/s")
            bot.reply_to(message, answer)
        else:
            bot.reply_to(message, "❌ Shahar topilmadi. Iltimos, nomini inglizcha yozib ko'ring (masalan: Tashkent).")
    
    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"]
    hum = response["main"]["humidity"]
    return f"📍 {city.capitalize()}\n🌡 Harorat: {temp}°C\n☁️ Holat: {desc}\n💧 Namlik: {hum}%"

# 4. BOT BUYRUQLARI
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Men 24/7 ishlaydigan obi-havo botiman. 🌤\nShahar nomini yozing (masalan: Chust yoki Tashkent):")

@bot.message_handler(func=lambda m: True)
def chat(message):
    weather_info = get_weather(message.text)
    bot.send_message(message.chat.id, weather_info)

# 5. ISHGA TUSHIRISH
if __name__ == "__main__":
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))).start()
    bot.infinity_polling()
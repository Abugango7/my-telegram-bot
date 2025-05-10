pyTelegramBotAPI
import telebot
from telebot import types

TOKEN = '7786037838:AAGcg2K71BGST67Gy5RQTXVTP1WTLoKVs0Q'  # bot tokeningiz
bot = telebot.TeleBot(TOKEN)

# Mahsulotlar ro'yxati
mahsulotlar = [
    "1. 1.5 cola - 5 blok",
    "2. 2L cola - 5 blok",
    "3. Qibray baqalashka - 5 blok",
    "4. Qibray shisha - 5 blok",
    "5. Fanta 1.5 - 5 blok",
    "6. Dido so'q detskiy 27 donali - 5 blok",
    "7. Dido so'q detskiy 40 donali - 5 blok",
    "8. Ark tea 1.5L o‘rmon mevali - 2 blok",
    "9. Ark tea 1.5L shaftoli - 1 blok"
]

# /start komandasi
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 Mahsulotlar", "📞 Kontakt yuborish")
    bot.send_message(message.chat.id, "Xush kelibsiz! Quyidagilardan birini tanlang:", reply_markup=markup)

# Mahsulot menyusi
@bot.message_handler(func=lambda m: m.text == "📦 Mahsulotlar")
def show_products(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for mahsulot in mahsulotlar:
        markup.add(mahsulot)
    
    markup.add("📞 Kontakt yuborish")
    bot.send_message(message.chat.id, "Mahsulotlardan birini tanlang:", reply_markup=markup)

# Kontakt va lokatsiya so‘rash
@bot.message_handler(func=lambda m: m.text == "📞 Kontakt yuborish")
def ask_contact(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(
        types.KeyboardButton("📱 Raqam yuborish", request_contact=True),
        types.KeyboardButton("📍 Lokatsiya yuborish", request_location=True)
    )
    bot.send_message(message.chat.id, "Raqamingiz yoki joylashuvingizni yuboring:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    bot.send_message(message.chat.id, f"Raqamingiz qabul qilindi: {message.contact.phone_number}")

@bot.message_handler(content_types=['location'])
def location_handler(message):
    lat = message.location.latitude
    lon = message.location.longitude
    bot.send_message(message.chat.id, f"Lokatsiyangiz qabul qilindi:\nLatitude: {lat}, Longitude: {lon}")

# Buyurtma berish
@bot.message_handler(func=lambda m: m.text in mahsulotlar)
def handle_order(message):
    buyurtma = message.text
    with open("buyurtmalar.txt", "a", encoding="utf-8") as f:
        f.write(f"{message.from_user.first_name}: {buyurtma}\n")
    bot.send_message(message.chat.id, f"✅ Buyurtma qabul qilindi:\n{buyurtma}")

# Botni ishga tushurish
bot.polling(none_stop=True, interval=0, timeout=20)

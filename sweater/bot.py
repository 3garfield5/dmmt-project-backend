import telebot

token = '6682288724:AAE_Fx70SF5ARuW4TEAhG4LDXxzYPOLYqGE'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!')

bot.infinity_polling()
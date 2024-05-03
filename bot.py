import telebot

from sweater import db

token = '6682288724:AAE_Fx70SF5ARuW4TEAhG4LDXxzYPOLYqGE'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот-помощник команды DMMT. /n'
                                      'Я отвечу на часто задаваемые вопросы /n'
                                      'и в случае серьезной поломки помогу связаться с разработчиками! /n')

@bot.message_handler(commands=['Q&A'])
def q_and_a(message):
    bot.send_message(message.chat.id, 'Выбери проблему, с которой ты столкнулся: /n'
                                      '1.')

bot.infinity_polling()
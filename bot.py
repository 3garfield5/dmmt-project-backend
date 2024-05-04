import telebot
from telebot import types

from sweater import db, app
from sweater.models import BagBot

token = '6682288724:AAE_Fx70SF5ARuW4TEAhG4LDXxzYPOLYqGE'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    req_btn = types.KeyboardButton('Оставить заявку')
    markup.add(req_btn)
    bot.send_message(message.chat.id, 'Привет! Я бот-помощник команды DMMT. \n'
                                      'С моей помощью вы можете связаться с моими разработчиками для того, чтобы сообщить о каком-то баге! \n'
                                      'После вы обязательно получите обратную связь по проблеме!',
                     reply_markup=markup)

    def name_users(message):
        if message.text == 'Оставить заявку':
            bot.reply_to(message, 'Сейчас мы поэтапно заполним заявку \n'
                                              'Скажите как вас зовут?', reply_markup=types.ReplyKeyboardRemove())

            def tg_users(message):
                bot.send_message(message.chat.id, 'Напишите ваш телеграмм, чтобы мы могли с вами связаться! \n'
                                                  '(в формате @telegram)')

                name = message.text


                def bag_users(message):
                    bot.send_message(message.chat.id, 'Напишите о том, какой баг вы нашли на нашем сайте (1000 знаков)\n'
                                                      'Мои разработчики обязательно разберутся с этой проблемой\n'
                                                      '(по возможности)')
                    tg = message.text

                    def table(message):
                        bag = message.text
                        with app.app_context():
                            new_req = BagBot(name=name, tg=tg, bag=bag)
                            db.session.add(new_req)
                            db.session.commit()
                        bot.send_message(message.chat.id, 'Спасибо, что оповестили нас о проблеме!\n'
                                                          'Именно вы делаете нас лучше! \n'
                                                          'Чтобы оставить новую заявку, напишите: /start')
                    bot.register_next_step_handler(message, table)
                bot.register_next_step_handler(message, bag_users)
            bot.register_next_step_handler(message, tg_users)
        else:
            bot.send_message(message.chat.id, 'Видимо вы что-то сделали не так и я не смог обработать ваш запрос! \n'
                                              'Напишите "Оставить заявку" корректно!')
            bot.register_next_step_handler(message, name_users)
    bot.register_next_step_handler(message, name_users)





bot.infinity_polling()
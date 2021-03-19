import telebot
import config
from telebot import types
import random
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Main Keyboard-menu
    damir_button = types.KeyboardButton('Дамир')
    dice_button = types.KeyboardButton('Кубик🎲')
    timur_button = types.KeyboardButton('Тимур')
    stats_button = types.KeyboardButton('Обязательства')

    markup.add(dice_button, damir_button, timur_button, stats_button)

    bot.send_message(message.chat.id, 'БОТ - РАСПРЕДЕЛИТЕЛЬ ДЕЛ', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def main(message):
    if message.text =='Кубик🎲':
        bot.send_message(message.chat.id, str(random.randint(1, 6)))
    elif message.text == 'Дамир':
        markup = types.InlineKeyboardMarkup(row_width=2)
        time1 = types.InlineKeyboardButton('10 минут', callback_data='10d')
        time2 = types.InlineKeyboardButton('20 минут', callback_data='20d')
        time3 = types.InlineKeyboardButton('30 минут', callback_data='30d')
        time4 = types.InlineKeyboardButton('40 минут', callback_data='40d')
        markup.add(time1, time2, time3, time4)
        bot.send_message(message.chat.id, 'Сколько минут Дамир потратил?', reply_markup=markup)
    elif message.text == 'Тимур':
        bot.send_message(message.chat.id, 'Сколько минут Тимур потратил?')
    elif message.text == 'Обязательства':
        bot.send_message(message.chat.id, 'Пока не умею(')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '10d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 10 минут!')
            elif call.data == '20d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 20 минут!')
            elif call.data == '30d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 30 минут!')
            elif call.data == '40d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 40 минут!')
    except Exception:
        pass


# RUN
bot.polling(True)

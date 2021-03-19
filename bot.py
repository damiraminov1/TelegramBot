import telebot
import config
from telebot import types
import random
import math
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Main Keyboard-menu
    damir_button = types.KeyboardButton('Дамир')
    dice_button = types.KeyboardButton('Кубик🎲')
    timur_button = types.KeyboardButton('Тимур')
    stats_button = types.KeyboardButton('Обязательства')

    markup.add(damir_button, dice_button, timur_button, stats_button)

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
        markup = types.InlineKeyboardMarkup(row_width=2)
        time1 = types.InlineKeyboardButton('10 минут', callback_data='10t')
        time2 = types.InlineKeyboardButton('20 минут', callback_data='20t')
        time3 = types.InlineKeyboardButton('30 минут', callback_data='30t')
        time4 = types.InlineKeyboardButton('40 минут', callback_data='40t')
        markup.add(time1, time2, time3, time4)
        bot.send_message(message.chat.id, 'Сколько минут Тимур потратил?', reply_markup=markup)

    elif message.text == 'Обязательства':
        data = open('data.txt')
        numeric_data = str(data.read())
        data.close()
        if int(numeric_data) > 0:
            bot.send_message(message.chat.id, 'Дамир должен Тимуру ' + str(numeric_data) + ' минут')
        elif int(numeric_data) < 0:
            bot.send_message(message.chat.id, 'Тимур должен Дамиру ' + str(abs(int(numeric_data))) + ' минут')
        elif int(numeric_data) == 0:
            bot.send_message(message.chat.id, 'Никто никому ничего не должен!')

def add_time(value, person):
    data = open('data.txt', 'r')
    numeric_data = int(str(data.read()))
    if person == 'damir':
        numeric_data -= value
    else:
        numeric_data += value
    data.close()
    wdata = open('data.txt', 'w')
    wdata.write(str(numeric_data))
    wdata.close()



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == '10d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 10 минут!')
                add_time(10, 'damir')
            elif call.data == '20d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 20 минут!')
                add_time(20, 'damir')
            elif call.data == '30d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 30 минут!')
                add_time(30, 'damir')
            elif call.data == '40d':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Дамиру 40 минут!')
                add_time(40, 'damir')
            elif call.data == '10t':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Тимуру 10 минут!')
                add_time(10, 'timur')
            elif call.data == '20t':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Тимуру 20 минут!')
                add_time(20, 'timur')
            elif call.data == '30t':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Тимуру 30 минут!')
                add_time(30, 'timur')
            elif call.data == '40t':
                bot.send_message(call.message.chat.id, 'Хорошо, я записал Тимуру 40 минут!')
                add_time(40, 'timur')

    except Exception:
        pass


# RUN
bot.polling(True)

import telebot
import config
from telebot import types
import random
import os

DATA_FILE_NAME = 'data.txt'
bot = telebot.TeleBot(config.TOKEN)

wait_minutes = False
name = None

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
    global name, wait_minutes

    if wait_minutes and message.text.isdigit():
        wait_minutes = False
        if name == 'd':
            full_name = 'Дамиру'
            db_name = 'damir'
        else:
            full_name = 'Тимуру'
            db_name = 'timur'
        minutes = int(message.text)
        bot.send_message(message.chat.id, 'Хорошо, я записал {} {} минут!'.format(full_name, minutes))
        add_time(minutes, db_name)
    elif message.text =='Кубик🎲':
        bot.send_message(message.chat.id, str(random.randint(1, 6)))
    elif message.text == 'Дамир':
        markup = types.InlineKeyboardMarkup(row_width=2)
        time1 = types.InlineKeyboardButton('10 минут', callback_data='10d')
        time2 = types.InlineKeyboardButton('20 минут', callback_data='20d')
        time3 = types.InlineKeyboardButton('30 минут', callback_data='30d')
        time4 = types.InlineKeyboardButton('40 минут', callback_data='40d')
        markup.add(time1, time2, time3, time4)
        bot.send_message(message.chat.id, 'Сколько минут Дамир потратил?', reply_markup=markup)
        name = 'd'
        wait_minutes = True
    elif message.text == 'Тимур':
        markup = types.InlineKeyboardMarkup(row_width=2)
        time1 = types.InlineKeyboardButton('10 минут', callback_data='10t')
        time2 = types.InlineKeyboardButton('20 минут', callback_data='20t')
        time3 = types.InlineKeyboardButton('30 минут', callback_data='30t')
        time4 = types.InlineKeyboardButton('40 минут', callback_data='40t')
        markup.add(time1, time2, time3, time4)
        bot.send_message(message.chat.id, 'Сколько минут Тимур потратил?', reply_markup=markup)
        name = 't'
        wait_minutes = True
    elif message.text == 'Обязательства':
        numeric_data = read_numeric_data()
        if numeric_data > 0:
            bot.send_message(message.chat.id, 'Дамир должен Тимуру ' + str(numeric_data) + ' минут')
        elif numeric_data < 0:
            bot.send_message(message.chat.id, 'Тимур должен Дамиру ' + str(abs(int(numeric_data))) + ' минут')
        elif numeric_data == 0:
            bot.send_message(message.chat.id, 'Никто никому ничего не должен!')

def add_time(value, person):
    numeric_data = read_numeric_data()
    if person == 'damir':
        numeric_data -= value
    else:
        numeric_data += value
    write_numeric_data(numeric_data)

def read_numeric_data():
    if os.path.isfile(DATA_FILE_NAME):
        data = open(DATA_FILE_NAME, 'r')
        return int(str(data.read()))
    else:
        return 0

def write_numeric_data(numeric_data):
    wdata = open(DATA_FILE_NAME, 'w')
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
import telebot
import config
from telebot import types
import random
import os

DATA_FILE_NAME = 'data.txt'
bot = telebot.TeleBot(config.TOKEN)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Main Keyboard-menu
time_markup_keyboard = types.InlineKeyboardMarkup(row_width=2)  # Time InLine Keyboard
name = None
wait_minutes = False
names = {'damir': 'Дамир', 'timur': 'Тимур'}
time_str_to_callback_data_dict = {'10 минут': '10', '20 минут': '20', '30 минут': '30', '40 минут': '40'}


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
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
        write_time(message.chat.id, int(message.text), view_data_after_editing=True)
    elif message.text =='Кубик🎲':
        dice(message)
    elif message.text == 'Дамир':
        name = 'damir'
        read_time(message)
    elif message.text == 'Тимур':
        name = 'timur'
        read_time(message)
    elif message.text == 'Обязательства':
        view_data(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data in time_str_to_callback_data_dict.values():
            write_time(call.message.chat.id, call.data, view_data_after_editing=True)
    delete_message(call)


def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def dice(message):
    global wait_minutes
    result = random.randint(1, 6)
    bot.send_message(message.chat.id, 'На кубике выпало: ' + (str(result)))
    if result in [1, 3, 5]:
        bot.send_message(message.chat.id, 'Делает {}!'.format(names['timur']))
    else:
        bot.send_message(message.chat.id, 'Делает {}!'.format(names['damir']))
    wait_minutes = False


def view_data(message_chat_id):
    global wait_minutes
    numeric_data = read_numeric_data()
    if numeric_data > 0:
        bot.send_message(message_chat_id, 'Дамир должен Тимуру ' + str(numeric_data) + ' минут')
    elif numeric_data < 0:
        bot.send_message(message_chat_id, 'Тимур должен Дамиру ' + str(abs(int(numeric_data))) + ' минут')
    elif numeric_data == 0:
        bot.send_message(message_chat_id, 'Никто никому ничего не должен!')
    wait_minutes = False
    if abs(int(numeric_data)) >= 60:
        bot.send_message(message_chat_id, 'Внимание! Достигнут предел долга 60 минут. Да здравствует власть!')


def read_time(message):
    global wait_minutes
    wait_minutes = True
    add_time_create_buttons()
    ask_minutes(message.chat.id)


def add_time_create_buttons():
    global time_markup_keyboard_not_added, time_markup_keyboard, name, time_str_to_callback_data_dict
    time_markup_keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons_time_list = ['time1', 'time2', 'time3', 'time4']
    for time_str in time_str_to_callback_data_dict:
        for button in buttons_time_list:
            button = types.InlineKeyboardButton(time_str, callback_data=time_str_to_callback_data_dict[time_str])
        time_markup_keyboard.add(button)
    time_markup_keyboard_not_added = False


def ask_minutes(message_chat_id):
    global name
    bot.send_message(message_chat_id, 'Сколько времени это заняло у {}?'.format(names[name]+'а'),
                     reply_markup=time_markup_keyboard)


def add_time(value):
    global name
    numeric_data = read_numeric_data()
    if name == 'damir':
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


def write_time(chat_id, minutes, view_data_after_editing=False):
    global wait_minutes
    if wait_minutes:
        bot.send_message(chat_id, 'Хорошо, я записал {} {} минут!'.format(names[name] + 'у', str(minutes)))
        add_time(int(str(minutes)))
        wait_minutes = False
    if view_data_after_editing:
        view_data(chat_id)


# RUN
bot.polling(True)

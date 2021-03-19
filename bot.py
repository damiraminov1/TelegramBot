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
    if message.text == 'Дамир':
        bot.send_message(message.chat.id, 'Сколько минут Дамир потратил?')
    if message.text == 'Тимур':
        bot.send_message(message.chat.id, 'Сколько минут Тимур потратил?')
    if message.text == 'Обязательства':
        bot.send_message(message.chat.id, 'Пока не умею(')

# RUN
bot.polling(True)

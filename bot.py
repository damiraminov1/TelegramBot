import telebot
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/welcome.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id,
                     'Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, бот созданный служить тебе.'.format(message.from_user, bot.get_me()))
    parse_mode ='html'

@bot.message_handler(content_types=['text'])
def answer(message):
    bot.send_message(message.chat.id, message.text)


# RUN
bot.polling(True)

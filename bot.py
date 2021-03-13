import telebot
import config
bot = telebot.TeleBot(config.TOKEN)
# RUN
bot.polling(True)

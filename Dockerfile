FROM python:3.9
WORKDIR /dice_telegram_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY / .
CMD [ "python", "./bot.py" ]
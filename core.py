import random
import telebot
import requests

from bs4 import BeautifulSoup

BOT_TOKEN = "5893852470:AAGwYLG5TYScXx6GZWbwb68bra--NDX3d5s"

bot = telebot.TeleBot(BOT_TOKEN)

time_frames = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]

url = "https://paper-trader.frwd.one/"


def get_image_url(trading_pair: str):
    req = requests.post(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 "
                          "Safari/537.36 "
        },
        data={
            "pair": trading_pair,
            "timeframe": random.choice(time_frames),
            "candles": random.randint(0, 1001),
            "ma": random.randint(0, 1001),
            "tp": random.randint(0, 101),
            "sl": random.randint(0, 101),
        },
    )
    img_url = (
        BeautifulSoup(req.text, "html.parser")
        .body.find("img")
        .get("src")
        .removeprefix("./")
    )
    return str(url + img_url)


@bot.message_handler(commands=["start"])
def say_hi(message):
    bot.send_message(
        message.chat.id, text="Send your trading pair, for example: BTCUSDT"
    )


@bot.message_handler(content_types=["text"])
def send_welcome(message):
    if all(map(str.isalpha, message.text)):
        try:
            bot.send_photo(message.chat.id, get_image_url(message.text))
        except Exception as e:
            print(e)
            bot.reply_to(message, "oooops :( Invalid trading pair")


bot.polling()

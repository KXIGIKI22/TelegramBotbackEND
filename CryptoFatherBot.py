# -*- coding: utf-8 -*-
from __future__ import annotations
import logging
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
#from telegram.ext.filters import Filters
from queue import Queue

# Ініціалізація логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для отримання курсу валют
def get_exchange_rate(currency):
    url = f"https://api.exchangerate-api.com/v4/latest/USD"  # Замініть USD на валюту, яку ви хочете отримати
    response = requests.get(url)
    data = response.json()

    if currency in data['rates']:
        return data['rates'][currency]
    else:
        return "Unknown currency"

# Функція для отримання курсу криптовалют
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    if crypto in data and 'usd' in data[crypto]:
        return data[crypto]['usd']
    else:
        return "Unknown currency"

# Функція для отримання погодних даних
def get_weather(city):
    api_key = "0c3a23b3418374fa864f71bcf3d5e018"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get('main') and data.get('weather'):
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Weather in city {city}: Temperature {temperature}°C, {description.capitalize()}"
    else:
        return "Could not get weather for this city."

# Функція для обробки команди /start
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hello, {user.first_name}! I'm your CryptoFatherBot. How can I assist you today?")

# Функція для обробки команди /commands
def commands(update: Update, context: CallbackContext):
    command_list = [
        "/start - Start using the bot",
        "/commands - List of available commands",
        "/exchange - Get exchange rates of currencies",
        "/weather - Get weather information of a city"
    ]
    update.message.reply_text("\n".join(command_list))

# Функція для обробки команди /exchange
def exchange(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter the currency code you want to know the exchange rate for.")

# Функція для обробки команди /weather
def weather(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter the city name to get the weather information.")

def main():
    # Створення черги оновлень
    update_queue = Queue()

    # Підключення до Telegram API за допомогою токену бота
    updater = Updater("6317225374:AAFe2L_CdrdvHpd0nXjv0dsznRoZwKXnNLs", use_context=True, update_queue=update_queue)

    # Отримання обробників команд та повідомлень
    dispatcher = updater.dispatcher

    # Додавання обробників команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("commands", commands))
    dispatcher.add_handler(CommandHandler("exchange", exchange))
    dispatcher.add_handler(CommandHandler("weather", weather))

    # Додавання обробників вибору валюти або криптовалюти з клавіатури
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, selected_currency))

    # Додавання обробника для отримання погоди за введеним містом
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_weather_for_city))

    # Запуск бота
    updater.start_polling()

    # Завершення роботи бота після натиснення Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
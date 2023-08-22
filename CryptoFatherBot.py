import logging
import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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
        return "Невідома валюта"


# Функція для отримання курсу криптовалют
def get_crypto_price(crypto):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    if crypto in data and 'usd' in data[crypto]:
        return data[crypto]['usd']
    else:
        return "Невідома криптовалюта"


# Функція для отримання погодних даних
def get_weather(city):
    api_key = "0c3a23b3418374fa864f71bcf3d5e018"  # Замініть на свій API-ключ
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get('main') and data.get('weather'):
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        return f"Погода у місті {city}: Температура {temperature}°C, {description.capitalize()}"
    else:
        return "Не вдалося отримати погоду для цього міста."


# ...

def main():
    # Підключення до Telegram API за допомогою токену бота
    updater = Updater("6317225374:AAFe2L_CdrdvHpd0nXjv0dsznRoZwKXnNLs")

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
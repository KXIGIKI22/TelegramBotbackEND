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


# Функція для обробки команди /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привіт! Я бот для отримання курсу валют. Введи /commands, щоб побачити список доступних команд.')


# Функція для обробки команди /commands
def commands(update: Update, context: CallbackContext) -> None:
    command_list = [
        "/start - Почати роботу з ботом",
        "/commands - Показати список доступних команд",
        "/exchange - Отримати курс валют",
        "/weather - Отримати погоду у введеному місті"
    ]
    update.message.reply_text('\n'.join(command_list))


# Функція для обробки команди /exchange
def exchange(update: Update, context: CallbackContext) -> None:
    # Створення клавіатури з кнопками
    keyboard = [
        [KeyboardButton("USD"), KeyboardButton("EUR")],
        [KeyboardButton("Bitcoin"), KeyboardButton("Ethereum")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    update.message.reply_text("Оберіть валюту або криптовалюту:", reply_markup=reply_markup)


# Функція для обробки вибору валюти або криптовалюти з клавіатури
def selected_currency(update: Update, context: CallbackContext) -> None:
    selected_currency = update.message.text
    if selected_currency in ["USD", "EUR", "Bitcoin", "Ethereum"]:
        if selected_currency in ["Bitcoin", "Ethereum"]:
            price = get_crypto_price(selected_currency.lower())
            update.message.reply_text(f"Поточна ціна {selected_currency}: {price} USD")
        else:
            rate = get_exchange_rate(selected_currency)
            update.message.reply_text(f"Поточний курс {selected_currency}: {rate}")
    else:
        update.message.reply_text("Невірно обрано валюту або криптовалюту.")


# Функція для обробки команди /weather
def weather(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введіть назву міста для перегляду погоди:")


# Функція для обробки повідомлень
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Ви відправили: " + update.message.text)


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

    # Запуск бота
    updater.start_polling()

    # Завершення роботи бота після натиснення Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
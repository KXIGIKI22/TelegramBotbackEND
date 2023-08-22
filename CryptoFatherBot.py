import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Ініціалізація логгера
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функція для обробки команди /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привіт! Я бот для отримання курсу валют. Введи /commands, щоб побачити список доступних команд.')

# Функція для обробки команди /commands
def commands(update: Update, context: CallbackContext) -> None:
    command_list = [
        "/start - Почати роботу з ботом",
        "/commands - Показати список доступних команд",
        "/exchange - Отримати курс валют",
        "/weather - Отримати погоду у введеному місті"
    ]
    update.message.reply_text('\n'.join(command_list))

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

    # Додавання обробників повідомлень
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    # Завершення роботи бота після натиснення Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
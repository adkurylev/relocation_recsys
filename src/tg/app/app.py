import logging
import locale

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ParseMode
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import text, bold

from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from utils import setup_logging

_logger = logging.getLogger(__name__)

def init_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())
    return bot, dp

bot, dp = init_bot()


@dp.message_handler(commands=["start"])
async def start(message: Message):
    start_keyboard = InlineKeyboardMarkup()


async def on_shutdown(dp):
    _logger.warning('Bye! Shutting down webhook connection')
    bot.close()


def main():
    setup_logging()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()





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
from settings import BOT_TOKEN

_logger = logging.getLogger(__name__)
action_clb = CallbackData('action_callback', 'action')


def init_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())
    return bot, dp

bot, dp = init_bot()


@dp.message_handler(commands=["start"])
async def start(message: Message):
    """
    Start message
    """
    # @TODO: replace on db request
    keyboard = InlineKeyboardMarkup()
    is_existing_user = False
    if not is_existing_user:
        keyboard.add(InlineKeyboardButton(text="Зарегистрироваться",
                                          callback_data=action_clb.new(action="register")))
        msg = "Вступительное слово и описание функционала здесь"
    else:
        #keyboard.add(InlineKeyboardButton(text="Посмотреть рекомендации",
        #                                  callback_data=action_clb.new(action="get_rec")))
        msg = "Вот что я могу тебе предложить"

    keyboard.add(InlineKeyboardButton(text="Посмотреть рекомендации",
                                      callback_data=action_clb.new(action="get_recommendation")))
    await message.answer(msg, reply_markup=keyboard)


@dp.callback_query_handler(action_clb.filter(action="register"))
async def register(query: CallbackQuery):
    # @TODO: post user request
    await bot.send_message(query.from_user.id, text="Вы успешно зарегистрированы")


@dp.callback_query_handler(action_clb.filter(action="get_recommendation"))
async def show_city(query: CallbackQuery):
    await bot.send_message(query.from_user.id, text="Щас что-нибудь поищу")


async def on_shutdown(dp):
    _logger.warning('Bye! Shutting down webhook connection')
    bot.close()


def main():
    setup_logging()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()

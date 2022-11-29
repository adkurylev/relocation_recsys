import logging
import locale
import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message, ParseMode
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import text, bold

from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from utils import setup_logging
from settings import BOT_TOKEN, RECSYS_URL, RECSYS_PORT, DB_URL, DB_PORT
import requests

_logger = logging.getLogger(__name__)
action_clb = CallbackData('action_callback', 'action')
reaction_clb = CallbackData("reaction_callback", "score", "city_id")

RECSYS_ADDRESS = "http://"+RECSYS_URL+":"+RECSYS_PORT
DB_ADDRESS = "http://"+DB_URL+":"+DB_PORT


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
    r = requests.post(DB_ADDRESS+"/user", json={"tg_id": query.from_user["id"]})
    # @TODO: post user request
    await bot.send_message(query.from_user.id, text="Вы успешно зарегистрированы")


@dp.callback_query_handler(action_clb.filter(action="get_recommendation"))
@dp.callback_query_handler(reaction_clb.filter())
async def show_city(query: CallbackQuery):

    data = query.data.split(":")
    if data[0] == "reaction_callback":
        r = requests.post(DB_ADDRESS+"/reaction", json={"city_id": data[2], "score": data[1],
                                                        "tg_id": query.from_user["id"]})
        if r.status_code == 200:
            query.answer("Записал")
        else:
            query.answer("Упс.. не смог сохранить результат")
            _logger.error("Can not save reaction")

    try:
        r = requests.get(RECSYS_ADDRESS+"/recommendation")
    except Exception as err:
        _logger.error(repr(err))
        raise err
    if r.status_code != 200:
        bot.send_message(query.from_user.id, text="Упс... Что-то пошло не так. Попробуйте зайти позднее")
        _logger.error("Recommendation service did not response properly")

    content = r.json()
    city_id = content["city_id"]
    msg = "Город: {:s} \n Описание: {:s} \n Номер города {:s}" \
        .format(content["city_name"], content["description"], city_id)

    keyboard = InlineKeyboardMarkup() \
                   .insert(InlineKeyboardButton(text="Up", callback_data=reaction_clb.new(score=1, city_id=city_id))) \
                   .insert(InlineKeyboardButton(text="So so", callback_data=reaction_clb.new(score=0, city_id=city_id)))  \
                   .insert(InlineKeyboardButton(text="Down", callback_data=reaction_clb.new(score=-1, city_id=city_id)))

    await bot.send_message(query.from_user.id, text=msg, reply_markup=keyboard)


async def on_shutdown(dp):
    _logger.warning('Bye! Shutting down webhook connection')
    bot.close()


def main():
    setup_logging()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()

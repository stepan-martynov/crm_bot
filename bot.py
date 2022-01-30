# import msilib
import config
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def start_answer(message: types.Message):
    await message.answer(f"И тебе, {message.from_user.username}, привет!")


@dp.message_handler()
async def echo_send(message: types.Message):
    if message.text == "Привет":

        await message.answer("И тебе привет!")
        await message.reply("Еще раз привет")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
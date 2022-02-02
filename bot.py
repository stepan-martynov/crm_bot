# import msilib
import config
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)



async def startup():
    print("Бот запущен")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup)
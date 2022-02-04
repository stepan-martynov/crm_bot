from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import config

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

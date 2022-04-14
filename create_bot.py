import os
import config
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
# print(os.getenv("POETRY_CRM_BOT_TOKEN"))
bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=storage)

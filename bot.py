# import msilib

from aiogram.utils import executor
from create_bot import dp


async def startup(_):
    print("Бот запущен")


import handlers

handlers.photographer.register_photographer_handler(dp)
handlers.other.register_other_hendlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup)

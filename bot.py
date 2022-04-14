# import msilib

from aiogram.utils import executor
from create_bot import dp


async def startup( ):
    print("Бот запущен")

from handlers import photographer, other, brocker

photographer.register_photographer_hendler(dp)
other.register_other_hendlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
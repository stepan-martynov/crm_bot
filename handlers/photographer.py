from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, Regexp
from aiogram import types
import re

class FSMCreateDos(StatesGroup):
    url = State()
    # doc_tamplate = State() #buttons
    # customer = State()
    service = State()
    location = State() #Buttons СПб ЛО
    # address = State()
    broker = State()
    price = State()


# Start FSM
yadisk_regexp = r'\nhttps://disk.yandex.\S+'

async def start_bill_request(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["url"] = re.match(yadisk_regexp, message.text)[0]
        await message.answer(f"Мы сохранили ссылку на ЯД"
                            f"\n{data['url']}"
                            f"\nТеперь выбери брокера")
    await FSMCreateDos.broker.set()


async def add_broker(message: types.Contact, state=FSMContext):
    async with state.proxy() as data:
        data["broker"] = message.contact.phone_number
    await message.reply("Теперь укажи стоимость услуги?")
    await FSMCreateDos.price.set()


async def add_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["price"] = int(message.text)
        await message.reply(str(data))
    await state.finish()


def register_photographer_hendler(dp: Dispatcher):
    # dp.register_message_handler(start_bill_request, Text(contains="https://disk.yandex"))
    dp.register_message_handler(start_bill_request, Regexp(yadisk_regexp), state=None)
    dp.register_message_handler(add_broker, content_types='contact', state=FSMCreateDos.broker)
    dp.register_message_handler(add_price, state=FSMCreateDos.price)

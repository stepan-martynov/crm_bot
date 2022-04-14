from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text, Regexp
import re


class FSMCreateDos(StatesGroup):
    url = State()
    # doc_tamplate = State() #buttons
    # customer = State()
    service = State()
    location = State()  # Buttons СПб ЛО
    # address = State()
    broker = State()
    price = State()


# Start FSM
yadisk_regexp = r'https://disk.yandex.ru/\S+'
yadisk_regexp_new = r'(?P<url>https?://[^\s]+)'


async def start_bill_request(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print(message.text)
        print(re.search(yadisk_regexp_new, message.text).group("url"))
        # print(re.match(yadisk_regexp, message.text))
        data["url"] = re.search(yadisk_regexp_new, message.text).group("url")
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
    dp.register_message_handler(start_bill_request, Text(contains="https://disk.yandex"))
    dp.register_message_handler(start_bill_request, Regexp(yadisk_regexp), state=None)
    dp.register_message_handler(add_broker, content_types='contact', state=FSMCreateDos.broker)
    dp.register_message_handler(add_price, state=FSMCreateDos.price)

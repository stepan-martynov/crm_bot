from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Regexp
import re

from keyboards import kb_service, kb_customer
import render_docx


class FSMCreateDos(StatesGroup):
    url = State()
    broker = State()
    customer = State()
    service = State()  # город / загород
    price = State()


# Start FSM
yadisk_regexp = r'(?P<url>https?://disk.yandex.ru[^\s]+)'


async def start_bill_request(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["url"] = re.search(yadisk_regexp, message.text).group("url")
        await message.answer(f"Мы сохранили ссылку на ЯД"
                             f"\n{data['url']}"
                             f"\nТеперь выбери брокера")
    await FSMCreateDos.broker.set()


async def add_broker(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        # data["broker_phone"] = message.contact.phone_number
        data["broker"] = f'{message.text}'
    await message.reply("Выбери заказчика?", reply_markup=kb_customer)
    await FSMCreateDos.customer.set()


# пока 2 брокера ев и ев прайвет.
async def set_customer(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["customer"] = message.text
    await message.reply("Выбери локацию?", reply_markup=kb_service)
    await FSMCreateDos.service.set()


async def set_service(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["service"] = message.text
    await message.reply("Укажи цену", reply_markup=ReplyKeyboardRemove())
    await FSMCreateDos.price.set()


async def add_price(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data["price"] = message.text
        ent = render_docx.OutEntity(**data)
        print(ent.exel_string)
        print(ent.portal_string)
        render_docx.render_doc(ent)
        # TODO f = doc.load()
        # TODO send docx file
        # TODO send info
        await message.reply(f'{ent.num}.docx сформирован')

    await state.finish()


def register_photographer_handler(dp: Dispatcher):
    dp.register_message_handler(start_bill_request, Regexp(yadisk_regexp), state=None)
    dp.register_message_handler(add_broker, state=FSMCreateDos.broker)
    dp.register_message_handler(set_customer, state=FSMCreateDos.customer)
    dp.register_message_handler(set_service, state=FSMCreateDos.service)
    dp.register_message_handler(add_price, state=FSMCreateDos.price)

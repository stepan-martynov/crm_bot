from aiogram import types, Dispatcher


async def start_bill_request(message: types.Message):
    await message.reply(f"Создадим счет?\n{message.text}")


def register_photographer_hendler(dp: Dispatcher):
    dp.register_message_handler(start_bill_request, lambda message: "yadi" in message.text)


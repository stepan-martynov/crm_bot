from aiogram import types, Dispatcher


async def start_command(message: types.Message):
    await message.reply(f"И тебе, {message.from_user.username}, привет!")


def register_other_hendlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start", ])

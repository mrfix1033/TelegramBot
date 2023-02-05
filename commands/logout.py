from aiogram.filters import Command
from aiogram.types import Message
from ..main import dp, data_file


@dp.message(Command(commands=['exit', 'logout']))
async def command_logout(msg: Message):
    id = msg.from_user.id
    if not data_file.is_logged(id):
        await msg.answer("Вы не вошли в систему. Напишите /login для входа")
    else:
        data_file.rem_logged(id)
        await msg.answer("Вы вышли из системы. Напишите /login для входа")
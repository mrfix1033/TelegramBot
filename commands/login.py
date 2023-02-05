from aiogram.filters import Command
from aiogram.types import Message
from ..main import dp, data_file


@dp.message(Command(commands=['login']))
async def command_login(msg: Message):
    splited = msg.text.split(" ", 1)
    args = splited[1].split(" ") if len(splited) == 2 else []
    if data_file.is_logged(msg.from_user.id):
        await msg.answer("Вы уже вошли в систему. Напишите /exit для выхода")
        return
    elif len(args) != 2:
        await msg.answer("/login [username] [password]")
        return
    user = args[0]
    password = args[1]
    if not data_file.is_user(user):
        await msg.answer("Такого пользователя нет")
    elif data_file.get_password(user) != password:
        await msg.answer("Неверный пароль")
    else:
        id = msg.from_user.id
        data_file.add_logged(id)
        await msg.answer(f"Здравствуйте, {user}")

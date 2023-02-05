from aiogram.filters import Command
from aiogram.types import Message
from ..main import dp


@dp.message(Command(commands=['help']))
async def command_help(msg: Message):
    await msg.answer("/lastupdates\n/help\n/animal\n/login (for developers)\n/exit (for developers)")
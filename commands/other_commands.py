from aiogram.types import Message
from ..main import dp


@dp.message()
async def other_commands(msg: Message):
    await msg.answer("bot don't work. use /help")

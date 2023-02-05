from aiogram.filters import Command
from aiogram.types import Message
from ..main import dp


@dp.message(Command(commands=['lastupdates']))
async def command_lastupdates(msg: Message):
    await msg.answer('''text=Команды:'
/lastupdates - посмотреть последние обновления
/resetmode - выйти из текущего режима
/animal - картинки с животными''')
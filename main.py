import dotenv

from .Data import Data
from aiogram import Bot, Dispatcher
import dotenv
import os

dotenv.load_dotenv()
BOT_TOKEN: str = os.getenv("TOKEN")
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
API_DOGS_URL: str = 'https://random.dog/woof.json'
API_FOXS_URL: str = 'https://randomfox.ca/floof/'
text: str = '''
Напиши:
"котики", чтобы посмотреть на котиков
"собачки" - чтобы посмотреть на собачек
"лисички" - чтобы посмотреть на лисичек'''
last_bot_updates = '\n'.join("""
Начата разработка этого бота
Добавлена команды""".split('\n')[-10:])

data_file = Data()
dp.run_polling(bot)

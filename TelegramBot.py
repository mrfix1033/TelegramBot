import os
import traceback
from random import randint
import requests
from environs import Env


from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, Message
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, F


class File:
    def __init__(self, filename, default):
        self.filename = filename
        self.default = default
        self.__create_if_not_exists()
        read = self.__read()
        try:
            self.data = eval(read)
        except Exception:
            traceback.print_exc()
            self.recreate()

    def __create_if_not_exists(self):
        if not os.path.exists(self.filename):
            self.create()

    def __read(self):
        with open(self.filename, encoding='utf8') as f:
            return f.read()

    def recreate(self):
        with open("old_" + self.filename, 'w', encoding='utf8') as f:
            f.write(self.__read())
        self.create()

    def create(self):
        with open(self.filename, 'w', encoding='utf8') as f:
            f.write(self.default)

    def write(self, data):
        with open(self.filename, 'w', encoding='utf8') as f:
            f.write(str(data))


class Data(File):
    def __init__(self):
        super().__init__("data.txt", """{"users": {}, "logged": []}""")
        try:
            self.users: dict = self.data['users']
            self.logged: list = self.data['logged']
        except Exception:
            traceback.print_exc()
            self.recreate()

    def add_logged(self, id):
        self.logged.append(id)
        self.save()

    def rem_logged(self, id):
        if self.is_logged(id):
            self.logged.remove(id)
            self.save()

    def is_logged(self, id):
        return id in self.logged

    def is_user(self, username):
        return username in self.users

    def get_password(self, username):
        return self.users.get(username)

    def save(self):
        data = {"users": self.users,
                "logged": self.logged}
        self.write(data)


class Keyboard:
    def __init__(self, *button_texts):
        self.keyboard = ReplyKeyboardMarkup()
        self.buttons = [KeyboardButton(i) for i in button_texts]
        self.keyboard.add(*self.buttons)


async def command_login(msg: Message):
    if data_file.is_logged(msg.from_user.id):
        await msg.answer("Вы уже вошли в систему. Напишите /logout для выхода")
        return
    splited = msg.text.split(" ", 1)
    args = splited[1].split(" ") if len(splited) == 2 else []
    if len(args) != 2:
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


async def command_logout(msg: Message):
    id = msg.from_user.id
    if not data_file.is_logged(id):
        await msg.answer("Вы не вошли в систему. Напишите /login для входа")
    else:
        data_file.rem_logged(id)
        await msg.answer("Вы вышли из системы. Напишите /login для входа")


async def command_animal(msg: Message):
    r = randint(0, 2)
    if r == 0:
        cat_response = requests.get(API_CATS_URL)
        cat_link = cat_response.json()['file']
        await msg.answer_photo(cat_link)
    elif r == 1:
        dog_response = requests.get(API_DOGS_URL)
        dog_link = dog_response.json()['url']
        await msg.answer_photo(dog_link)
    elif r == 2:
        fox_response = requests.get(API_FOXS_URL)
        fox_link = fox_response.json()['link']
        await msg.answer_photo(fox_link)


async def command_help(msg: Message):
    await msg.answer("/lastupdates\n/help\n/animal\n/login (for developers)\n/logout (for developers)")


async def command_lastupdates(msg: Message):
    await msg.answer('''
Добавлены команды (/help)
Ведется разработка новых фич''')


async def photo_handler(msg: Message):
    await msg.answer_photo(msg.photo[2].file_id)
    await msg.answer("you sent photo")


async def voice_handler(msg: Message):
    await msg.answer_voice(msg.voice.file_id)
    await msg.answer("you sent voice")


async def audio_handler(msg: Message):
    await msg.answer_audio(msg.audio.file_id)
    await msg.answer("you sent audio")


async def sticker_handler(msg: Message):
    await msg.answer_audio(msg.sticker.file_id)
    await msg.answer("you sent sticker")


async def other_commands(msg: Message):
    await msg.answer("bot don't work. use /help")


API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://aws.random.cat/meow'
API_DOGS_URL: str = 'https://random.dog/woof.json'
API_FOXS_URL: str = 'https://randomfox.ca/floof/'

env = Env()
env.read_env()
BOT_TOKEN: str = env('TOKEN')
data_file = Data()
bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

dp.message.register(command_animal, Command(commands=['animal']))
dp.message.register(command_help, Command(commands=['help']))
dp.message.register(command_lastupdates, Command(commands=['lastupdates']))
dp.message.register(command_login, Command(commands=['login']))
dp.message.register(command_logout, Command(commands=['logout']))
dp.message.register(photo_handler, F.photo)
dp.message.register(voice_handler, F.voice)
dp.message.register(audio_handler, F.audio)
dp.message.register(sticker_handler, F.sticker)
dp.message.register(other_commands)

dp.run_polling(bot)

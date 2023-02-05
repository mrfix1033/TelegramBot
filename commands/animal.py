import requests
from random import randint
from aiogram.filters import Command
from aiogram.types import Message
from ..main import dp, API_CATS_URL, API_DOGS_URL, API_FOXS_URL


@dp.message(Command(commands=['animal']))
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

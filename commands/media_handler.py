from aiogram import F
from aiogram.types import Message
from ..main import dp


@dp.message(F.photo)
async def photo_handler(msg: Message):
    await msg.answer_photo(msg.photo[2].file_id)
    await msg.answer("you sent photo")


@dp.message(F.voice)
async def voice_handler(msg: Message):
    await msg.answer("you sent voice")


@dp.message(F.audio)
async def audio_handler(msg: Message):
    await msg.answer("you sent audio")

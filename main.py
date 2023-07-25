import os

from aiogram import Bot, Dispatcher, types, executor
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(os.environ.get("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('HI')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

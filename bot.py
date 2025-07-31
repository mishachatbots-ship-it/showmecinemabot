import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import random
import pandas as pd

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def start_handler(message: Message):
    user = message.from_user
    await message.answer("Привет, я ЧтоБыПосмотретьБот")
    # print(f"user with id: {user.id} /start")

@dp.message(Command(commands=['mood']))
async def mood_handler(message: Message):
    user = message.from_user
    await message.answer("Какое настроение?")

@dp.message(Command(commands=['tip']))
async def tip_handler(message: Message):
    user = message.from_user
    await message.answer("Я не очень умный, поэтому мне нужны ключевые слова\nНапример:")
    await message.answer("Посоветуй мне фильм")
    await message.answer("Я хочу посмотреть кино")

filter_list = ["фильм", "кино", "cinema", "картина"]
@dp.message(F.text.func(lambda text: any(word in text.lower() for word in filter_list)))
async def text_message_handler(message: Message):
    user = message.from_user
    ind, cin = data_import()
    await message.answer(cin)
    # msg = await message.reply('хуёх')

@dp.message(~F.text.func(lambda text: any(word in text.lower() for word in filter_list)))
async def text_message_handler(message: Message):
    user = message.from_user
    await message.answer('Я почти готов дать тебе совет, тебе надо только попросить')

def data_import():
    df = pd.read_excel('showmecinema_bot_data.xlsx')
    ind = random.randrange(1, df.shape[0]+1)
    return [ind, str(df.iloc[ind, 0])]

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
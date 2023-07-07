import asyncio

from config import BOT_TOKEN
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from day3_async_requests_aiohttp import AnimalAPIRequester


def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)

    user_ids = set()

    @dp.message_handler(commands=['start'])
    async def start_handler(message: types.Message):
        user_ids.add(message.chat.id)
        await message.answer("Welcome to a anonymous chat bot")

    @dp.message_handler()
    async def message_handler(message: types.Message):
        """Handles all non-command messages by sending them to other users"""
        tasks = []
        for uid in user_ids:
            if uid != message.chat.id:
                tasks.append(message.copy_to(uid))
        await asyncio.gather(*tasks)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

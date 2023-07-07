from config import BOT_TOKEN
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from day3_async_requests_aiohttp import AnimalAPIRequester


def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot)
    cat_requester = AnimalAPIRequester('cat')
    dog_requester = AnimalAPIRequester('dog')

    @dp.message_handler(commands=['start'])
    async def start_handler(message: types.Message):
        """Handler for messages"""
        await message.answer("Welcome to a text echo-bot")

    @dp.message_handler(commands=['cat'])
    async def send_cat(message: types.Message):
        """Replies with a cat"""
        chat_id = message.chat.id
        cat_url = (await cat_requester.get_urls(1))[0]
        await bot.send_photo(chat_id, cat_url)

    @dp.message_handler(commands=['dog'])
    async def send_dog(message: types.Message):
        """Replies with a dog"""
        chat_id = message.chat.id
        dog_url = (await dog_requester.get_urls(1))[0]
        await bot.send_photo(chat_id, dog_url)

    @dp.message_handler()
    async def echo(message: types.Message):
        """Echoes the message back"""
        await message.answer(message.text)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

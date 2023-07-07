import asyncio
from typing import Dict, Set, Tuple

from config import BOT_TOKEN
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from day3_async_requests_aiohttp import AnimalAPIRequester


class User:
    def __init__(self):
        pass


def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    waiting_users: Set[int] = set()
    user_pairings: Set[Tuple[int, int]] = set()

    @dp.message_handler(commands=['start'], state='*')
    async def start_handler(message: types.Message, state: FSMContext):
        """Handler for the start command"""
        await state.set_state("name")
        await message.answer("Welcome to a chat roulette, say your name")

    @dp.message_handler(state="name")
    async def name_asking(message: types.Message, state: FSMContext):
        name = message.text
        await state.update_data({"name": name})
        await state.set_state("age")
        await message.answer(f"Your name is set to {name}, tell us your age")

    @dp.message_handler(state="age")
    async def age_asking(message: types.Message, state: FSMContext):
        age = message.text
        if not age.isdigit():
            await message.answer("Your age should be a number")
        else:
            age = int(age)
            if age < 18 or age > 130:
                await message.answer("Enter valid age")
            else:
                await state.update_data({"age": age})
                name = (await state.get_data())['name']
                await state.set_state('ready')
                await message.answer(f"{name}, now you are ready to chat, write /chat to chat")

    @dp.message_handler(commands=['chat'], state="ready")
    async def chat_handler(message: types.Message, state: FSMContext):
        uid = message.chat.id
        if True:
            pass
        if len(waiting_users) == 0:
            waiting_users.add(uid)
            await message.answer("You will soon be paired to somebody, please wait")
        else:
            match_id = waiting_users.pop()
            user_pairings.add((uid, match_id))
            await state.set_state("chatting")
            await message.answer("You are paired to another user")
            await bot.send_message(match_id, "You are paired to another user")


    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

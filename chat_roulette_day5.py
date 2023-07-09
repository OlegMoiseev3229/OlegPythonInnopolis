from typing import Dict, Set, Tuple

from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


class User:
    def __init__(self):
        pass


def main():
    roulette_button = KeyboardButton("1 on 1")
    group_button = KeyboardButton("Group chat")
    choose_chat_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).insert(roulette_button).insert(group_button)

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
            if age < 14 or age > 130:
                await message.answer("Enter valid age")
            else:
                await state.update_data({"age": age})
                name = (await state.get_data())['name']
                await state.set_state('ready')
                await message.answer(f"{name}, now you are ready to chat, how do you want to chat",
                                     reply_markup=choose_chat_keyboard)

    @dp.message_handler(commands=['chat_r'], state="ready")
    async def chat_handler(message: types.Message, state: FSMContext):
        uid = message.chat.id
        if len(waiting_users) == 0:
            waiting_users.add(uid)
            await message.answer("You will soon be paired to somebody, please wait")
        else:
            match_id = waiting_users.pop()
            match_state = dp.current_state(chat=match_id, user=match_id)
            match_name = (await match_state.get_data())["name"]
            name = (await state.get_data())["name"]
            user_pairings.add((uid, match_id))
            await state.set_state("chatting")
            await message.answer(f"You are paired to another user: {match_name}. To disconnect type /close")
            await match_state.set_state("chatting")
            await bot.send_message(match_id, f"You are paired to another user: {name}. To disconnect type /close")

    @dp.message_handler(commands=['chat_g'], state="ready")
    async def group_chat_handler(message: types.Message, state: FSMContext):
        raise NotImplemented()

    @dp.message_handler(commands=['close'], state="chatting")
    async def close_handler(message: types.Message, state: FSMContext):
        uid = message.chat.id
        match_id = None
        for id1, id2 in user_pairings:
            if id1 == uid:
                match_id = id2
                user_pairings.remove((id1, id2))
                break
            if id2 == uid:
                match_id = id1
                user_pairings.remove((id1, id2))
                break
        match_state = dp.current_state(chat=match_id, user=match_id)

        match_name = (await match_state.get_data())["name"]
        name = (await state.get_data())["name"]

        await state.set_state("ready")
        await match_state.set_state("ready")
        await message.answer(f"You are successfully disconnected")
        await bot.send_message(match_id, f"The other user has disconnected")
        await message.answer(f"{name}, are ready to chat, write /chat to chat")
        await bot.send_message(match_id, f"{match_name}, are ready to chat, write /chat to chat")

    @dp.message_handler(state="chatting")
    async def chat_handler(message: types.Message, state: FSMContext):
        uid = message.chat.id
        match_id = None
        for id1, id2 in user_pairings:
            if id1 == uid:
                match_id = id2
                break
            if id2 == uid:
                match_id = id1
                break
        text = message.text
        name = (await state.get_data())["name"]
        await bot.send_message(match_id, f"{name}: {text}")

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

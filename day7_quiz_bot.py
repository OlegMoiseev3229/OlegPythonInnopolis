from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup,\
    ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


class Question:
    FIRST = 0
    SECOND = 1

    def __init__(self, text, first, second, correct,):
        self.text = text
        self.correct = correct
        self.first = first
        self.second = second

    def validate(self, answer):
        return answer == self.correct


def main():
    y_n_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    y_button = KeyboardButton("Yes")
    n_button = KeyboardButton("No")
    y_n_keyboard.insert(y_button).insert(n_button)

    questions = (
        Question("Are cows birds?", "Cows are cows", "Brds", Question.FIRST),
        Question("Who wrote 'Enter Sandman'?", "Beatles", "Metallica", Question.SECOND),
        Question("Yes?", "Yes", "No", Question.FIRST)
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    def update_buttons(question: Question):
        y_button.text = question.first
        n_button.text = question.second

    @dp.message_handler(commands=['start'], state="*")
    async def start_handler(message: types.Message, state: FSMContext):
        await message.answer("Welcome to our quiz")
        await state.set_state("quiz")
        await state.update_data({"current_question": 0, "points": 0})
        update_buttons(questions[0])
        await message.answer(questions[0].text, reply_markup=y_n_keyboard)

    @dp.message_handler(state="quiz")
    async def answer_handler(message: types.Message, state: FSMContext):
        ans = message.text
        current = (await state.get_data())["current_question"]
        points = (await state.get_data())["points"]
        question = questions[current]
        if ans == question.first:
            correct = question.validate(Question.FIRST)
        elif ans == question.second:
            correct = question.validate(Question.SECOND)
        else:
            await message.answer("Enter correct answer")
            print(question.first, question.second)
            return

        if correct:
            await message.answer("correct")
            points += 1
        else:
            await message.answer("incorrect")

        await state.update_data({"points": points})

        current += 1
        await state.update_data({"current_question": current})

        if current >= len(questions):
            await state.set_state("end")
            await message.answer(f"The end, You got {points}/{len(questions)} points",
                                 reply_markup=ReplyKeyboardRemove())
        else:
            question = questions[current]
            update_buttons(question)
            await message.answer(question.text, reply_markup=y_n_keyboard)

    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()

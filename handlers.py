from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from questions import quiz_data
from database import save_result, get_result

router = Router()

# Храним прогресс и счёт пользователей
user_scores = {}
user_progress = {}

@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! 👋 Это квиз-бот.\n"
        "Напиши /quiz чтобы начать игру.\n"
        "Напиши /stats чтобы посмотреть свой последний результат."
    )

@router.message(Command("quiz"))
async def start_quiz(message: types.Message):
    user_id = message.from_user.id
    user_scores[user_id] = 0
    user_progress[user_id] = 0
    await send_question(message, user_id)

async def send_question(message, user_id):
    idx = user_progress[user_id]

    # Если вопросы закончились
    if idx >= len(quiz_data):
        score = user_scores[user_id]
        save_result(user_id, score)
        await message.answer(
            f"Квиз завершён! 🎉\nВаш результат: {score} из {len(quiz_data)}"
        )
        return

    question = quiz_data[idx]

    # Генерация кнопок
    buttons = [
        [InlineKeyboardButton(text=option, callback_data=option)]
        for option in question["options"]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(question["question"], reply_markup=kb)

@router.callback_query()
async def handle_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    idx = user_progress[user_id]
    question = quiz_data[idx]
    answer = callback.data

    # Подтверждаем нажатие кнопки (обязательно в Aiogram 3)
    await callback.answer()

    # Убираем кнопки после ответа
    await callback.message.edit_reply_markup(reply_markup=None)

    # Сообщаем выбор пользователя
    await callback.message.answer(f"Вы выбрали: {answer}")

    # Проверка правильного ответа
    if answer == question["answer"]:
        user_scores[user_id] += 1

    # Переход к следующему вопросу
    user_progress[user_id] += 1
    await send_question(callback.message, user_id)

@router.message(Command("stats"))
async def stats(message: types.Message):
    score = get_result(message.from_user.id)
    if score is None:
        await message.answer("Вы ещё не проходили квиз.")
    else:
        await message.answer(f"Ваш последний результат: {score} из {len(quiz_data)}")

import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

# -----------------------------
# Получение токена через переменную окружения
# -----------------------------
API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Задайте переменную окружения с токеном.")

bot = Bot(token=API_TOKEN)
router = Dispatcher(storage=MemoryStorage())

# Словарь для пользователей, оставляющих фидбек
feedback_users = {}

# ---------- Клавиатуры ----------
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="⚛️ ATLANT 3D")]],
    resize_keyboard=True
)

main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🧠 Что мы делаем")],
        [types.KeyboardButton(text="🧪 Где используется")],
        [types.KeyboardButton(text="👥 Для кого")],
        [types.KeyboardButton(text="📩 Связаться с нами")],
        [types.KeyboardButton(text="💬 Оставить фидбек")]
    ],
    resize_keyboard=True
)

back_to_menu = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="🏠 Главное меню")]],
    resize_keyboard=True
)

# ---------- /start ----------
@router.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    print(f"NEW USER → ID:{user.id}, @{user.username}, {user.first_name}")

    welcome_text = (
        "\n\n\n\n\n"
        "🎮 *Мы — команда PvP, или портал в ад.*\n\n"
        "Нам важен ваш фидбек, чтобы делать наш стартап лучше.\n\n"
        "Нажмите кнопку ниже, чтобы узнать больше о нашем стартапе."
    )
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )

# ---------- Кнопка ATLANT 3D ----------
@router.message(F.text == "⚛️ ATLANT 3D")
async def open_menu(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu)

# ---------- Другие кнопки ----------
@router.message(F.text == "🧠 Что мы делаем")
async def what_we_do(message: types.Message):
    await message.answer(
        "PvP — deep tech стартап, создающий технологию атомной печати "
        "для микро- и наноструктур без дорогих фабрик.",
        reply_markup=back_to_menu
    )

@router.message(F.text == "🧪 Где используется")
async def where_used(message: types.Message):
    await message.answer(
        "Сферы применения PvP:\n"
        "• сенсоры\n"
        "• микроэлектроника\n"
        "• фотоника\n"
        "• космические технологии",
        reply_markup=back_to_menu
    )

@router.message(F.text == "👥 Для кого")
async def for_whom(message: types.Message):
    await message.answer(
        "Наше решение для:\n"
        "• инженеров и R&D команд\n"
        "• стартапов\n"
        "• университетов и лабораторий\n"
        "• технологических компаний",
        reply_markup=back_to_menu
    )

@router.message(F.text == "📩 Связаться с нами")
async def contact(message: types.Message):
    await message.answer(
        "Связаться с нами можно через Telegram:\n"
        "• @duu_sk (Founder)\n"
        "• @palenuch (CO-Founder)",
        reply_markup=back_to_menu
    )

# ---------- Фидбек ----------
@router.message(F.text == "💬 Оставить фидбек")
async def ask_feedback(message: types.Message):
    await message.answer("Напишите ваш фидбек в ответ на это сообщение.")
    feedback_users[message.from_user.id] = True

# ---------- Универсальный обработчик ----------
@router.message()
async def handle_all_messages(message: types.Message):
    user_id = message.from_user.id
    text = message.text

    # Кнопка "Главное меню"
    if text == "🏠 Главное меню":
        await message.answer("Главное меню:", reply_markup=main_menu)
        return

    # Фидбек
    if feedback_users.get(user_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = message.from_user
        print(f"[{now}] FEEDBACK → ID:{user.id}, @{user.username}, {user.first_name}: {text}")
        await message.answer("Спасибо за ваш фидбек! ❤️", reply_markup=main_menu)
        feedback_users.pop(user_id)
        return

# ---------- Запуск бота ----------
async def main():
    await router.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

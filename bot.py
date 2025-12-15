import asyncio
import os
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# -----------------------------
# Завантажуємо змінні оточення з .env
# -----------------------------
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
GOOGLE_CREDS_JSON_PATH = os.getenv("GOOGLE_CREDS_JSON_PATH")

if not API_TOKEN:
    raise ValueError("BOT_TOKEN не заданий! Задайте змінну оточення в .env")

bot = Bot(token=API_TOKEN)
router = Dispatcher(storage=MemoryStorage())
feedback_users = {}

# ---------- Клавіатури ----------
start_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="⚛️ PvP")]],
    resize_keyboard=True
)

main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🧠 Що ми робимо")],
        [types.KeyboardButton(text="🧪 Де використовується")],
        [types.KeyboardButton(text="👥 Для кого")],
        [types.KeyboardButton(text="📩 Зв’язатися з нами")],
        [types.KeyboardButton(text="💬 Залишити фідбек")]
    ],
    resize_keyboard=True
)

back_to_menu = types.ReplyKeyboardMarkup(
    keyboard=[[types.KeyboardButton(text="🏠 Головне меню")]],
    resize_keyboard=True
)

# ---------- /start ----------
@router.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    print(f"НОВИЙ КОРИСТУВАЧ → ID:{user.id}, @{user.username}, {user.first_name}")
    welcome_text = (
        "🎮 *Ми — команда PvP, або портал в пекло.*\n\n"
        "Нам важливий ваш фідбек.\n"
        "Натисніть кнопку нижче, щоб дізнатися більше."
    )
    await message.answer(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=start_keyboard
    )

# ---------- Кнопки ----------
@router.message(F.text == "⚛️ PvP")
async def open_menu(message: types.Message):
    await message.answer("Головне меню:", reply_markup=main_menu)

@router.message(F.text == "🧠 Що ми робимо")
async def what_we_do(message: types.Message):
    await message.answer("PvP — deep tech стартап...", reply_markup=back_to_menu)

@router.message(F.text == "🧪 Де використовується")
async def where_used(message: types.Message):
    await message.answer("Сфери застосування...", reply_markup=back_to_menu)

@router.message(F.text == "👥 Для кого")
async def for_whom(message: types.Message):
    await message.answer("Для кого рішення...", reply_markup=back_to_menu)

@router.message(F.text == "📩 Зв’язатися з нами")
async def contact(message: types.Message):
    await message.answer("Контакти Founder/CO-Founder", reply_markup=back_to_menu)

@router.message(F.text == "💬 Залишити фідбек")
async def ask_feedback(message: types.Message):
    await message.answer("Напишіть свій фідбек у відповідь на це повідомлення.")
    feedback_users[message.from_user.id] = True

@router.message()
async def handle_all_messages(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    if text == "🏠 Головне меню":
        await message.answer("Головне меню:", reply_markup=main_menu)
        return
    if feedback_users.get(user_id):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{now}] FEEDBACK → ID:{user_id}: {text}")
        await message.answer("Дякуємо за фідбек! ❤️", reply_markup=main_menu)
        feedback_users.pop(user_id)

# ---------- Запуск бота ----------
async def main():
    await router.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

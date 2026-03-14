import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from course_data import (
    WELCOME_TEXT, ABOUT_TEXT, MODULES_TEXT,
    TARIFFS_TEXT, WHAT_YOU_GET_TEXT, FAQ_LIST,
)
from keyboards import (
    main_menu_keyboard, back_keyboard, faq_keyboard,
    faq_back_keyboard, buy_keyboard, cancel_ai_keyboard,
)
from ai_helper import get_ai_response
from database import init_db, save_user, save_message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_LINK = os.getenv("PAYMENT_LINK", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Tracks which users are currently in AI-question mode
waiting_for_ai_question: set[int] = set()


# ── /start ────────────────────────────────────────────────────────────────────

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await save_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
    )
    await message.answer(
        text=WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )


# ── Inline button callbacks ───────────────────────────────────────────────────

@dp.callback_query(F.data == "about")
async def cb_about(call: CallbackQuery):
    await call.message.edit_text(
        text=ABOUT_TEXT,
        reply_markup=back_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "modules")
async def cb_modules(call: CallbackQuery):
    await call.message.edit_text(
        text=MODULES_TEXT,
        reply_markup=back_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "tariffs")
async def cb_tariffs(call: CallbackQuery):
    await call.message.edit_text(
        text=TARIFFS_TEXT,
        reply_markup=back_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "what_you_get")
async def cb_what_you_get(call: CallbackQuery):
    await call.message.edit_text(
        text=WHAT_YOU_GET_TEXT,
        reply_markup=back_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "faq")
async def cb_faq(call: CallbackQuery):
    await call.message.edit_text(
        text="❓ <b>Часто задаваемые вопросы</b>\n\nВыбери вопрос, который тебя интересует:",
        reply_markup=faq_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data.startswith("faq_"))
async def cb_faq_item(call: CallbackQuery):
    index = int(call.data.split("_")[1])
    if 0 <= index < len(FAQ_LIST):
        item = FAQ_LIST[index]
        text = f"{item['question']}\n\n{item['answer']}"
        await call.message.edit_text(
            text=text,
            reply_markup=faq_back_keyboard(),
            parse_mode="HTML",
        )
    await call.answer()


@dp.callback_query(F.data == "buy")
async def cb_buy(call: CallbackQuery):
    text = (
        "🛒 <b>Купить курс</b>\n\n"
        "Нажми кнопку ниже, чтобы перейти к оплате.\n"
        "После оплаты тебе откроется доступ ко всем материалам."
    )
    await call.message.edit_text(
        text=text,
        reply_markup=buy_keyboard(PAYMENT_LINK),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "ask_ai")
async def cb_ask_ai(call: CallbackQuery):
    waiting_for_ai_question.add(call.from_user.id)
    await call.message.edit_text(
        text=(
            "🤖 <b>Спросить AI</b>\n\n"
            "Напиши свой вопрос, и я отвечу на него с помощью искусственного интеллекта.\n\n"
            "Например: <i>Что такое воронка продаж?</i>"
        ),
        reply_markup=cancel_ai_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


@dp.callback_query(F.data == "back_to_menu")
async def cb_back_to_menu(call: CallbackQuery):
    waiting_for_ai_question.discard(call.from_user.id)
    await call.message.edit_text(
        text=WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML",
    )
    await call.answer()


# ── Free text messages (AI mode) ──────────────────────────────────────────────

@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    if user_id in waiting_for_ai_question:
        waiting_for_ai_question.discard(user_id)
        await save_message(user_id=user_id, text=message.text or "")

        thinking = await message.answer("🤖 Думаю над ответом...")
        answer = await get_ai_response(message.text or "")
        await thinking.delete()

        await message.answer(
            text=f"🤖 <b>Ответ AI:</b>\n\n{answer}",
            reply_markup=back_keyboard(),
            parse_mode="HTML",
        )
    else:
        await message.answer(
            text="Воспользуйся меню ниже 👇",
            reply_markup=main_menu_keyboard(),
        )


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    await init_db()
    print("✅ Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

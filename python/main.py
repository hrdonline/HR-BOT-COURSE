import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.storage.memory import MemoryStorage

from course_data import (
    COURSE_DESCRIPTION,
    MODULES_TEXT,
    TARIFFS_TEXT,
    WHAT_YOU_GET_TEXT,
    FAQ_LIST
)

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(storage=MemoryStorage())
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 О курсе", callback_data="about")],
        [InlineKeyboardButton(text="🗓 Программа модулей", callback_data="modules")],
        [InlineKeyboardButton(text="💰 Тарифы и цены", callback_data="tariffs")],
        [InlineKeyboardButton(text="🎁 Что вы получите", callback_data="whatyouget")],
        [InlineKeyboardButton(text="❓ Частые вопросы", callback_data="faq_menu")],
        [InlineKeyboardButton(text="💳 Записаться на курс", callback_data="buy")],
        [InlineKeyboardButton(text="💬 Задать вопрос ИИ", callback_data="ask_ai")],
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="menu")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я помощник курса *«ИИ в HR. Практика»*\n"
        "Автор: Зинаида Чумакова\n\n"
        "_Курс по книге, которой ещё нет в продаже_\n\n"
        "Старт 14 апреля 2026 · 8 недель · Онлайн\n\n"
        "Выбери что тебя интересует 👇",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer("Главное меню 👇", reply_markup=main_menu())

@dp.callback_query(F.data == "menu")
async def cb_menu(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню 👇", reply_markup=main_menu())

@dp.callback_query(F.data == "about")
async def cb_about(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 *ИИ в HR. Практика*\n"
        "_Курс по книге, которой ещё нет в продаже_\n\n"
        "Восемь недель. Семь модулей. Весь путь сотрудника — от найма до офбординга.\n\n"
        "Вы учитесь у HRD с 20-летним опытом в федеральных и международных компаниях.\n\n"
        "📅 Старт: 14 апреля 2026\n"
        "⏱ 8 недель · 7 модулей · 16 сессий\n"
        "🎓 Онлайн, вторник и четверг 19:00–21:00 МСК\n\n"
        "💥 Ранняя цена до 25 марта 2026!",
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "modules")
async def cb_modules(callback: CallbackQuery):
    await callback.message.edit_text(
        "🗓 *Программа курса:*\n\n"
        "▪️ Модуль 1 · Основы ИИ в HR — 14 и 16 апреля\n"
        "▪️ Модуль 2 · Привлечение и отбор — 21 и 23 апреля\n"
        "▪️ Модуль 3 · Адаптация и развитие — 28 и 30 апреля\n"
        "▪️ Модуль 4 · Эффективность и аналитика — 5 и 7 мая\n"
        "▪️ Модуль 5 · HR операции и КЭДО — 12 и 14 мая\n"
        "▪️ Модуль 6 · Вовлечённость и бренд — 19 и 21 мая\n"
        "▪️ Модуль 7 · Стратегический HR — 26 и 28 мая\n"
        "▪️ Финальный блок — 2 и 4 июня\n"
        "★ Защита проектов — 11 июня",
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "tariffs")
async def cb_tariffs(callback: CallbackQuery):
    await callback.message.edit_text(
        "💰 *Тарифы курса*\n"
        "_ранняя цена до 25 марта 2026_\n\n"
        "*Один модуль* — 8 800 ₽ (потом 10 000 ₽)\n"
        "Две сессии выбранного модуля + запись + материалы + 1 глава книги\n\n"
        "*Базовый* — 25 500 ₽ (потом 29 000 ₽)\n"
        "Все 16 сессий + записи + материалы + все главы книги + чат участников\n\n"
        "*Стандарт* — 39 600 ₽ (потом 45 000 ₽)\n"
        "Всё из Базового + защита проекта + сертификат\n\n"
        "*VIP* — 66 000 ₽ (потом 75 000 ₽)\n"
        "Всё из Стандарт + 2 индивидуальных занятия + 5 личных консультаций с Зинаидой",
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "whatyouget")
async def cb_whatyouget(callback: CallbackQuery):
    await callback.message.edit_text(
        "🎁 *Что вы получите:*\n\n"
        "📖 Главы книги до выхода в издательстве\n"
        "🛠 Промпт-киты под каждый HR-процесс\n"
        "📋 Чек-листы и шаблоны для внедрения ИИ\n"
        "💼 Практикумы, которые можно применить сразу\n"
        "🎯 Свой проект внедрения ИИ в HR\n"
        "🤝 Чат участников (тарифы Базовый и выше)\n\n"
        "🤖 *6 типов ИИ которые разберёте:*\n"
        "• Генеративный ИИ\n"
        "• Предиктивный ИИ\n"
        "• People Analytics\n"
        "• ONA — анализ неформальных связей\n"
        "• Агентный ИИ\n"
        "• Skills Intelligence",
        reply_markup=back_menu(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "faq_menu")
async def cb_faq_menu(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❓ Для кого этот курс?", callback_data="faq_0")],
        [InlineKeyboardButton(text="❓ Нужны технические знания?", callback_data="faq_1")],
        [InlineKeyboardButton(text="❓ Это курс про ChatGPT?", callback_data="faq_2")],
        [InlineKeyboardButton(text="❓ Когда старт и расписание?", callback_data="faq_3")],
        [InlineKeyboardButton(text="❓ Что если пропущу занятие?", callback_data="faq_4")],
        [InlineKeyboardButton(text="❓ Сколько стоит?", callback_data="faq_5")],
        [InlineKeyboardButton(text="❓ Есть ли рассрочка?", callback_data="faq_6")],
        [InlineKeyboardButton(text="❓ Как оплатить?", callback_data="faq_7")],
        [InlineKeyboardButton(text="❓ Про книгу", callback_data="faq_8")],
        [InlineKeyboardButton(text="❓ Будет ли сертификат?", callback_data="faq_9")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="menu")],
    ])
    await callback.message.edit_text("❓ *Частые вопросы* — выбери нужный:", reply_markup=kb, parse_mode="Markdown")

FAQ_ANSWERS = [
    ("Для кого этот курс?", "Для любого уровня HR и любой специализации: рекрутёров, HR-менеджеров, HRBP, специалистов по C&B и HR-директоров. Технических знаний не нужно — достаточно желания разобраться."),
    ("Нужны технические знания?", "Нет! Достаточно уверенно пользоваться компьютером. Все инструменты разбираем с нуля и сразу на примерах из HR."),
    ("Это курс про ChatGPT?", "Нет. Курс про ИИ в широком смысле: генеративный, предиктивный, People Analytics, агентный ИИ и Skills Intelligence — всё через реальные HR-задачи."),
    ("Когда старт и расписание?", "Старт 14 апреля 2026. Занятия каждый вторник и четверг в 19:00–21:00 МСК. 8 недель, 16 сессий. Все записи сохраняются."),
    ("Что если пропущу занятие?", "Запись будет доступна через несколько часов после сессии. Доступ к записям — до конца августа 2026."),
    ("Сколько стоит?", "До 25 марта 2026 ранняя цена:\n• Один модуль — 8 800 ₽\n• Базовый — 25 500 ₽\n• Стандарт — 39 600 ₽\n• VIP — 66 000 ₽\nПосле 25 марта цены вырастают на 12-14%."),
    ("Есть ли рассрочка?", "Рассрочка рассматривается индивидуально. Напишите @ZinaidaChu или @Averkieva_Helen — обсудим вариант."),
    ("Как оплатить?", "Зинаида выставляет счёт по реквизитам. Напишите @ZinaidaChu или @Averkieva_Helen, укажите тариф и email — счёт придёт в течение дня."),
    ("Про книгу", "Книга «ИИ в HR. Руководство по работе с интеллектом» ещё не вышла в издательстве. Участники первого потока получают главы по одной после каждого модуля — это эксклюзив!"),
    ("Будет ли сертификат?", "Да, для тарифов Стандарт и VIP. Нужно защитить проект 11 июня. Сертификат подтверждает прохождение программы и защиту практического проекта."),
]

@dp.callback_query(F.data.startswith("faq_"))
async def cb_faq(callback: CallbackQuery):
    idx = int(callback.data.replace("faq_", ""))
    question, answer = FAQ_ANSWERS[idx]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад к вопросам", callback_data="faq_menu")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")],
    ])
    await callback.message.edit_text(
        f"❓ *{question}*\n\n{answer}",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "buy")
async def cb_buy(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать Зинаиде", url="https://t.me/ZinaidaChu")],
        [InlineKeyboardButton(text="✍️ Написать Елене", url="https://t.me/Averkieva_Helen")],
        [InlineKeyboardButton(text="◀️ В главное меню", callback_data="menu")],
    ])
    await callback.message.edit_text(
        "💳 *Записаться на курс*\n\n"
        "Старт: 14 апреля 2026\n\n"
        "⏰ *Ранняя цена до 25 марта:*\n"
        "• Один модуль — 8 800 ₽\n"
        "• Базовый — 25 500 ₽\n"
        "• Стандарт — 39 600 ₽\n"
        "• VIP — 66 000 ₽\n\n"
        "Напишите Зинаиде или Елене — помогут выбрать тариф и выставят счёт 🙌",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "ask_ai")
async def cb_ask_ai(callback: CallbackQuery):
    await callback.message.edit_text(
        "💬 *Режим вопросов*\n\n"
        "Напиши свой вопрос — отвечу!\n\n"
        "Для возврата в меню напиши /menu",
        parse_mode="Markdown"
    )

@dp.message(F.text)
async def text_handler(message: Message):
    thinking = await message.answer("⏳ Думаю...")

    try:
        from mistralai import Mistral
        client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

        system_prompt = f"""Ты тёплый и дружелюбный помощник курса «ИИ в HR. Практика» Зинаиды Чумаковой.
Отвечай только на русском языке. Отвечай кратко и по делу.
Для записи всегда отправляй к @ZinaidaChu или @Averkieva_Helen.

ИНФОРМАЦИЯ О КУРСЕ:
{COURSE_DESCRIPTION}

ПРОГРАММА МОДУЛЕЙ:
{MODULES_TEXT}

ТАРИФЫ:
{TARIFFS_TEXT}

ЧТО ПОЛУЧАТ УЧАСТНИКИ:
{WHAT_YOU_GET_TEXT}
"""

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message.text}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        answer = response.choices[0].message.content
        print(f"Mistral OK: {answer[:50]}")

    except Exception as e:
        print(f"Mistral ERROR: {type(e).__name__}: {e}")
        answer = (
            "Что-то пошло не так 😔\n\n"
            "Напишите напрямую — ответим быстро!\n"
            "👉 @ZinaidaChu или @Averkieva_Helen"
        )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Написать Зинаиде", url="https://t.me/ZinaidaChu")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="menu")],
    ])

    await thinking.delete()
    await message.answer(answer, reply_markup=kb)

async def main():
    print("✅ Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

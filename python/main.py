import sys
print("=== БОТА ЗАПУСКАЕМ ===", flush=True)
print(f"Python: {sys.version}", flush=True)
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery
)
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")

router = Router()

# ============ ТАРИФЫ ============
# Цены в копейках (1 руб = 100 копеек)
TARIFFS = {
    "module": {
        "name": "📚 Один модуль",
        "price": 880000,       # 8 800 ₽
        "label": "8 800 ₽",
        "full_price": "10 000 ₽",
        "description": (
            "✅ Сессии одного модуля (2 встречи)\n"
            "✅ Запись сессий\n"
            "✅ Материалы встреч\n"
            "✅ Одна глава книги по теме модуля\n\n"
            "⚡ Ранняя цена до 25 марта!"
        )
    },
    "basic": {
        "name": "🎓 Базовый",
        "price": 2550000,      # 25 500 ₽
        "label": "25 500 ₽",
        "full_price": "29 000 ₽",
        "description": (
            "✅ Все 7 модулей + финальный блок\n"
            "✅ Запись всех сессий\n"
            "✅ Материалы всех встреч\n"
            "✅ Чат участников\n"
            "✅ Все главы книги\n\n"
            "⚡ Ранняя цена до 25 марта!"
        )
    },
    "standard": {
        "name": "⭐ Стандарт",
        "price": 3960000,      # 39 600 ₽
        "label": "39 600 ₽",
        "full_price": "45 000 ₽",
        "description": (
            "✅ Всё из тарифа Базовый\n"
            "✅ Защита проекта (11 июня)\n"
            "✅ Сертификат об окончании\n\n"
            "⚡ Ранняя цена до 25 марта!"
        )
    },
    "vip": {
        "name": "💎 VIP",
        "price": 6600000,      # 66 000 ₽
        "label": "66 000 ₽",
        "full_price": "75 000 ₽",
        "description": (
            "✅ Всё из тарифа Стандарт\n"
            "✅ 2 индивидуальных занятия с Зинаидой\n"
            "✅ 5 личных консультаций по HR и ИИ\n"
            "✅ Личная стратегия внедрения ИИ\n\n"
            "⚡ Ранняя цена до 25 марта!"
        )
    }
}

# ============ КЛАВИАТУРЫ ============

def main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📖 О курсе", callback_data="about"),
            InlineKeyboardButton(text="📅 Программа", callback_data="program")
        ],
        [InlineKeyboardButton(text="💰 Тарифы и оплата", callback_data="tariffs")],
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="faq"),
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")
        ]
    ])

def tariffs_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Один модуль — 8 800 ₽", callback_data="buy_module")],
        [InlineKeyboardButton(text="🎓 Базовый — 25 500 ₽", callback_data="buy_basic")],
        [InlineKeyboardButton(text="⭐ Стандарт — 39 600 ₽", callback_data="buy_standard")],
        [InlineKeyboardButton(text="💎 VIP — 66 000 ₽", callback_data="buy_vip")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_main")]
    ])

def back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Главное меню", callback_data="back_main")]
    ])

def buy_keyboard(tariff_key: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить сейчас", callback_data=f"pay_{tariff_key}")],
        [InlineKeyboardButton(text="◀️ К тарифам", callback_data="tariffs")]
    ])

# ============ ХЭНДЛЕРЫ ============

@router.message(CommandStart())
async def cmd_start(message: Message):
    text = (
        "👋 Привет! Я бот курса\n\n"
        "🧠 *«ИИ в HR. Практика»*\n"
        "_Курс по книге, которой ещё нет в продаже_\n\n"
        "👩‍💼 Автор: *Зинаида Чумакова*\n"
        "HRD с 20-летним опытом в федеральных и международных компаниях\n\n"
        "📅 Старт: *14 апреля*\n"
        "⏱ Длительность: *8 недель · 7 модулей*\n"
        "🌐 Формат: *Онлайн, вт и чт 19:00–21:00 МСК*\n\n"
        "⚡ *Ранняя цена действует до 25 марта!*\n\n"
        "Выбери, что тебя интересует 👇"
    )
    await message.answer(text, parse_mode="Markdown", reply_markup=main_keyboard())


@router.callback_query(F.data == "back_main")
async def back_main(callback: CallbackQuery):
    text = (
        "🧠 *«ИИ в HR. Практика»*\n"
        "_Курс по книге, которой ещё нет в продаже_\n\n"
        "📅 Старт: *14 апреля* · ⏱ *8 недель*\n"
        "⚡ *Ранняя цена до 25 марта!*\n\n"
        "Выбери, что тебя интересует 👇"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=main_keyboard())
    await callback.answer()


@router.callback_query(F.data == "about")
async def about_course(callback: CallbackQuery):
    text = (
        "📖 *О курсе «ИИ в HR. Практика»*\n\n"
        "Восемь недель. Семь модулей. Весь путь сотрудника — "
        "от первого касания до финального разговора.\n\n"
        "🎯 *Для кого:*\n"
        "• Рекрутёры\n"
        "• HR-менеджеры и HR-дженералисты\n"
        "• HR-бизнес-партнёры\n"
        "• Специалисты по C&B\n"
        "• HR-директора\n"
        "• Все, кто хочет понять как ИИ меняет HR\n\n"
        "🏆 *Уникальность курса:*\n"
        "Вы учитесь не у человека, который изучил ИИ и решил "
        "рассказать про HR. Вы учитесь у HRD с 20-летним опытом "
        "в федеральных и международных компаниях.\n\n"
        "📚 *Что вы получите:*\n"
        "• Промпт-киты под каждый HR-процесс\n"
        "• Чек-листы и шаблоны для внедрения ИИ\n"
        "• Практикумы, применимые сразу\n"
        "• Свой проект внедрения ИИ\n"
        "• Главы книги до выхода в издательстве\n\n"
        "🤖 *6 типов ИИ, которые разберёте:*\n"
        "Генеративный · Предиктивный · People Analytics\n"
        "ONA · Агентный ИИ · Skills Intelligence\n\n"
        "📅 *Занятия:* вторник и четверг, 19:00–21:00 МСК"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_keyboard())
    await callback.answer()


@router.callback_query(F.data == "program")
async def program(callback: CallbackQuery):
    text = (
        "📅 *Программа — 7 модулей · 16 сессий · 8 недель*\n\n"
        "📌 *Модуль 1* — Основы ИИ в HR\n"
        "_14 и 16 апреля_\n"
        "Карта ИИ-ландшафта, 6 типов ИИ, путь сотрудника, этика\n\n"
        "📌 *Модуль 2* — Привлечение и отбор\n"
        "_21 и 23 апреля_\n"
        "Бренд работодателя, скрининг резюме, интервью, оффер, пребординг\n\n"
        "📌 *Модуль 3* — Адаптация и развитие\n"
        "_28 и 30 апреля_\n"
        "Онбординг, первые 30-60-90 дней, обучение, карта навыков\n\n"
        "📌 *Модуль 4* — Эффективность и аналитика\n"
        "_5 и 7 мая_\n"
        "Цели, оценка эффективности, HR-аналитика, вознаграждения\n\n"
        "📌 *Модуль 5* — HR операции и КЭДО\n"
        "_12 и 14 мая_\n"
        "Документооборот, self-service, чат-боты, офбординг\n\n"
        "📌 *Модуль 6* — Вовлечённость и бренд\n"
        "_19 и 21 мая_\n"
        "Пульс-опросы, Sentiment Analysis, внутренние коммуникации\n\n"
        "📌 *Модуль 7* — Стратегический HR\n"
        "_26 и 27 мая_\n"
        "Кадровое планирование, агентный ИИ, HR-команда будущего\n\n"
        "🏁 *Финальный блок* — 2 и 4 июня\n"
        "⭐ *Защита проектов* — 11 июня\n"
        "🏅 Вручение сертификатов"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_keyboard())
    await callback.answer()


@router.callback_query(F.data == "tariffs")
async def tariffs(callback: CallbackQuery):
    text = (
        "💰 *Тарифы курса*\n\n"
        "⚡ *Ранняя цена действует до 25 марта!*\n\n"
        "📚 *Один модуль* — 8 800 ₽\n"
        "~~10 000 ₽~~ · Попробовать на конкретной задаче\n\n"
        "🎓 *Базовый* — 25 500 ₽\n"
        "~~29 000 ₽~~ · Пройти весь путь самостоятельно\n\n"
        "⭐ *Стандарт* — 39 600 ₽\n"
        "~~45 000 ₽~~ · Весь путь + сертификат\n\n"
        "💎 *VIP* — 66 000 ₽\n"
        "~~75 000 ₽~~ · Весь путь + сертификат + личная работа с Зинаидой\n\n"
        "👇 Выберите тариф для оплаты:"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=tariffs_keyboard())
    await callback.answer()


@router.callback_query(F.data.in_(["buy_module", "buy_basic", "buy_standard", "buy_vip"]))
async def show_tariff(callback: CallbackQuery):
    tariff_key = callback.data.replace("buy_", "")
    tariff = TARIFFS[tariff_key]

    text = (
        f"*{tariff['name']}*\n\n"
        f"💰 Стоимость: *{tariff['label']}* ~~{tariff['full_price']}~~\n\n"
        f"{tariff['description']}"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=buy_keyboard(tariff_key))
    await callback.answer()


@router.callback_query(F.data.startswith("pay_"))
async def send_invoice(callback: CallbackQuery, bot: Bot):
    tariff_key = callback.data.replace("pay_", "")
    tariff = TARIFFS[tariff_key]

    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title=f"Курс «ИИ в HR. Практика» — {tariff['name']}",
        description=(
            f"Автор: Зинаида Чумакова\n"
            f"Старт: 14 апреля 2026\n"
            f"Формат: Онлайн\n"
            f"Тариф: {tariff['name']}"
        ),
        payload=f"course_{tariff_key}",
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label=tariff['name'], amount=tariff['price'])],
        start_parameter=f"buy_{tariff_key}",
        need_name=True,
        need_email=True,
    )
    await callback.answer()


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    tariff_key = message.successful_payment.invoice_payload.replace("course_", "")
    tariff = TARIFFS.get(tariff_key, {})
    tariff_name = tariff.get("name", "")

    text = (
        f"🎉 *Оплата прошла успешно!*\n\n"
        f"Спасибо за покупку тарифа *{tariff_name}*!\n\n"
        f"📩 *Следующий шаг:*\n"
        f"Напишите Елене @Averkieva_Helen или Зинаиде @ZinaidaChu — "
        f"они пришлют вам доступы и всю информацию.\n\n"
        f"📅 Старт курса: *14 апреля*\n"
        f"До встречи на курсе! 🚀"
    )
    await message.answer(text, parse_mode="Markdown")


@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    text = (
        "❓ *Часто задаваемые вопросы*\n\n"
        "🔹 *Нужны ли технические знания?*\n"
        "Нет. Достаточно уверенно пользоваться компьютером. "
        "Все инструменты разбираем с нуля.\n\n"
        "🔹 *Это курс про ChatGPT?*\n"
        "Нет. Курс про ИИ в широком смысле — через конкретные HR-задачи. "
        "Генеративные модели — лишь часть программы.\n\n"
        "🔹 *Сколько времени нужно в неделю?*\n"
        "4 часа в прямом эфире (вт и чт, 19:00–21:00 МСК) "
        "+ время на записи и проект.\n\n"
        "🔹 *Что если пропущу сессию?*\n"
        "Запись будет доступна через несколько часов после окончания.\n\n"
        "🔹 *Как долго доступны записи?*\n"
        "До конца августа 2026.\n\n"
        "🔹 *Нужно ли покупать книгу отдельно?*\n"
        "Нет. Главы входят в тарифы Базовый, Стандарт и VIP.\n\n"
        "🔹 *Можно сначала купить Базовый, потом доплатить до Стандарт?*\n"
        "Да, доплата возможна без переплат.\n\n"
        "🔹 *Есть ли рассрочка?*\n"
        "Рассматривается индивидуально. Напишите @ZinaidaChu.\n\n"
        "🔹 *Есть ли корпоративный формат?*\n"
        "Да, двухдневная программа для команды. "
        "Стоимость обсуждается индивидуально."
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_keyboard())
    await callback.answer()


@router.callback_query(F.data == "contacts")
async def contacts(callback: CallbackQuery):
    text = (
        "📞 *Контакты*\n\n"
        "👩‍💼 *Зинаида Чумакова* — автор курса\n"
        "Telegram: @ZinaidaChu\n"
        "Канал: t.me/chumakova_HRD\n\n"
        "👩‍💼 *Елена Аверкиева* — организационные вопросы\n"
        "Telegram: @Averkieva_Helen\n\n"
        "📱 Телефон: +7 924 101 2664\n\n"
        "⏱ _Отвечаем в течение рабочего дня!_"
    )
    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=back_keyboard())
    await callback.answer()


# ============ ЗАПУСК ============

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

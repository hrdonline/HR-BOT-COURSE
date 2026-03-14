from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="📌 О курсе", callback_data="about"),
            InlineKeyboardButton(text="📚 Модули", callback_data="modules"),
        ],
        [
            InlineKeyboardButton(text="💎 Тарифы", callback_data="tariffs"),
            InlineKeyboardButton(text="🎁 Что вы получите", callback_data="what_you_get"),
        ],
        [
            InlineKeyboardButton(text="❓ FAQ", callback_data="faq"),
            InlineKeyboardButton(text="🤖 Спросить AI", callback_data="ask_ai"),
        ],
        [
            InlineKeyboardButton(text="🛒 Купить курс", callback_data="buy"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])


def faq_keyboard() -> InlineKeyboardMarkup:
    from course_data import FAQ_LIST
    buttons = []
    for i, item in enumerate(FAQ_LIST):
        buttons.append([
            InlineKeyboardButton(text=item["question"], callback_data=f"faq_{i}")
        ])
    buttons.append([
        InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def faq_back_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ К списку FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_menu")],
    ])


def buy_keyboard(payment_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Оплатить курс", url=payment_link)],
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")],
    ])


def cancel_ai_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад в меню", callback_data="back_to_menu")]
    ])

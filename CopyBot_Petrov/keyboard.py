from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def main_reply_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text="Вимкнути бота ❌")
    b2 = KeyboardButton(text="Переглянути БД 📄")
    b3 = KeyboardButton(text="Переглянути БД(fast) 📄")
    kb.add(b1).add(b2).add(b3)
    return kb

def bot_turnoff_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Так ✅', callback_data='turnoff_accept')],
        [InlineKeyboardButton('Ні ❌', callback_data='turnoff_cancel')]
    ])
    return ikb

def database_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Всі пости', callback_data='database_all')],
        [InlineKeyboardButton('Опрацьовані пости', callback_data='database_processed')],
        [InlineKeyboardButton('Не опрацьовані пости', callback_data='database_notprocessed')]
    ])
    return ikb
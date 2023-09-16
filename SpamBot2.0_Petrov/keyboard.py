from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def main_reply_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text="Вимкнути бота ❌")
    b2 = KeyboardButton(text="Почати розсилку 🧨")
    b3 = KeyboardButton(text="Аккаунти 💭")
    b4 = KeyboardButton(text="Переглянути БД 📄")
    kb.add(b1).add(b2).add(b3).insert(b4)
    return kb

def check_banned(session, phone_number) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Спам Бан', callback_data=f'ban_spam_{session}_{phone_number}')],
        [InlineKeyboardButton('Бан аккаунта', callback_data=f'ban_completely_{session}_{phone_number}')],
    ])
    return ikb

def bot_turnoff_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Так ✅', callback_data='turnoff_accept')],
        [InlineKeyboardButton('Ні ❌', callback_data='turnoff_cancel')]
    ])
    return ikb
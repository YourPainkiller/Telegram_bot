from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bot_keyboard1 = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
)

button_check_rate = KeyboardButton('Узнать курс')
bot_keyboard1.insert(button_check_rate)
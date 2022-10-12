from aiogram import types
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

admin_inline_keyboad = InlineKeyboardMarkup()
admin_inline_button1 = InlineKeyboardButton(text="Добавить вопрос",callback_data="quesion")
admin_inline_button2 = InlineKeyboardButton(text="Произвести рассылку по пользователям",callback_data="sender")
admin_inline_button3 = InlineKeyboardButton(text="Просмотр отзывов",callback_data="feedback")

admin_inline_keyboad.add(admin_inline_button1).add(admin_inline_button2)


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-01:00", callback_data="num_-1"),
            types.InlineKeyboardButton(text="-00:15", callback_data="num_-15"),
            types.InlineKeyboardButton(text="+00:15", callback_data="num_+15"),
            types.InlineKeyboardButton(text="+01:00", callback_data="num_+1"),
            
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

menu_greet = [
    [InlineKeyboardButton(text="📝 Предоставить доступ к аккаунту", callback_data="registration")]
]

menu_main = [
    [InlineKeyboardButton(text="📝 Добавить чела", callback_data="add_contact"),
     InlineKeyboardButton(text="🖼 Удалить чела", callback_data="delete_contact")],
    [InlineKeyboardButton(text="💳 Добавить сообщение по расписанию", callback_data="add_regular_massage")],
    [InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]
]

menu_greet = InlineKeyboardMarkup(inline_keyboard=menu_greet)
menu_main = InlineKeyboardMarkup(inline_keyboard=menu_main)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

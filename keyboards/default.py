from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Sovrinlar"), KeyboardButton(text="🏆 Reyting TOP 15")],
        [KeyboardButton(text="📊 Mening natijam"), KeyboardButton(text="🤝 Do‘stni taklif et")],
    ],
    resize_keyboard=True
)

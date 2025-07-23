from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()


@router.message(F.text == "🤝 Do‘stni taklif et")
async def invite_friend_handler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    bot_username = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user_id}"

    text = (
        f"📢 <b>{full_name}</b>, do‘stlaringizni taklif qiling va sovrin yutish imkoniyatini oshiring!\n\n"
        f"🤝 Sizning taklif havolangiz:\n"
        f"<code>{referral_link}</code>\n\n"
        f"📌 Har bir taklif qilgan do‘stingiz uchun sizga +1 ball beriladi!"
    )

    # Ulashish uchun inline tugma
    share_button = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📤 Do‘stlarga ulashish",
                url=f"https://t.me/share/url?url={referral_link}&text=Keling, tanlovda qatnashaylik!"
            )
        ]
    ])

    await message.answer(text, reply_markup=share_button, parse_mode="HTML")

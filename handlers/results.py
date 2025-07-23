from aiogram import Router, types, F
from database.db import db
from database import queries

router = Router()


@router.message(F.text == "📊 Mening natijam")
async def my_result(message: types.Message):
    telegram_id = message.from_user.id

    # Foydalanuvchi haqida ma’lumotni olish
    user_data = db.fetchone(queries.GET_USER_STATS, (telegram_id,))

    if not user_data:
        await message.answer("Siz hali ro‘yxatdan o‘tmagansiz.")
        return

    full_name, username, invite_count, invited_by = user_data

    # Taklif qilgan foydalanuvchilar soni
    response = f"📊 <b>Sizning natijangiz:</b>\n\n"
    response += f"👤 Ism: {full_name}\n"
    response += f"🔗 Taklif qilgan do‘stlaringiz soni: <b>{invite_count}</b>\n"

    if invited_by:
        referrer_info = db.fetchone(queries.GET_REFERRER_INFO, (invited_by,))
        if referrer_info:
            ref_name, ref_username = referrer_info
            response += f"\n👥 Sizni taklif qilgan: {ref_name} (@{ref_username})"

    await message.answer(response)

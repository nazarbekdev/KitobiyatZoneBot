from aiogram import Router, types, F
from database.db import db
from database import queries

router = Router()


@router.message(F.text == "🏆 Reyting TOP 15")
async def top_15_handler(message: types.Message):
    users = db.fetchall(queries.GET_TOP_15_USERS)

    if not users:
        await message.answer("📊 Hozircha reytingda foydalanuvchilar yo‘q.")
        return

    text = "🏆 <b>TOP 15 Taklifchilar</b>\n\n"
    for i, (full_name, username, invite_count) in enumerate(users, start=1):
        name_display = f"{full_name} (@{username})" if username else full_name
        text += f"{i}. {name_display} — <b>{invite_count}</b> ta taklif\n"

    await message.answer(text, parse_mode="HTML")

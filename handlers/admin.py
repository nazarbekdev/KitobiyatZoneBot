from aiogram import Router, types
from aiogram.filters import Command
from database.db import db
from config import ADMIN_ID

router = Router()


@router.message(Command("count_user"))
async def count_users_handler(message: types.Message):
    if message.from_user.id not in (int(ADMIN_ID), 5605407368):
        await message.answer("⛔ Sizga bu buyruqni bajarishga ruxsat yo'q!")
        return
    else:
        query = "SELECT COUNT(*) FROM users;"
        result = db.fetchone(query)

        user_count = result[0] if result else 0

        await message.answer(f"📊 Botda ro‘yxatdan o‘tgan foydalanuvchilar soni: <b>{user_count}</b>", parse_mode="HTML")

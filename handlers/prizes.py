from aiogram import Router, F
from config import CHANNEL_USERNAME, PRIZE_POST_ID  # .env dan olingan
from aiogram.types import Message

router = Router()


@router.message(F.text == "🎁 Sovrinlar")
async def show_prizes_handler(message: Message):
    try:
        await message.bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=CHANNEL_USERNAME,
            message_id=PRIZE_POST_ID
        )
    except Exception as e:
        await message.answer("❌ Sovrinlar haqida maʼlumotni yuborishda xatolik yuz berdi.")
        print(f"[ERROR] Sovrinlar postini yuborishda xatolik: {e}")

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, CommandObject
from aiogram.exceptions import TelegramBadRequest

from config import CHANNEL_USERNAME
from database.db import db
from database import queries
from keyboards.default import main_menu

router = Router()


async def is_user_subscribed(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except TelegramBadRequest:
        return False


@router.message(CommandStart(deep_link=True))
@router.message(CommandStart())
async def start_handler(message: Message, command: CommandObject):
    user = message.from_user
    telegram_id = user.id
    full_name = user.full_name
    username = user.username or ""

    referrer_id = command.args  # referral link orqali kelgan bo‘lsa

    # 🧠 Avval ro‘yxatdan o‘tganmi?
    existing_user = db.fetchone(queries.GET_USER_BY_TELEGRAM_ID, (telegram_id,))

    if not existing_user:
        invited_by = int(referrer_id) if referrer_id and referrer_id.isdigit() and int(
            referrer_id) != telegram_id else None

        # 📝 Yangi foydalanuvchini bazaga yozish
        db.execute(
            queries.REGISTER_USER,
            (telegram_id, full_name, username, invited_by)
        )

        # 🧮 Agar referal bo‘lsa, uning taklif sonini oshirish
        if invited_by:
            db.execute(queries.INCREMENT_INVITE_COUNT, (invited_by,))

        await message.answer("🎉 Botga xush kelibsiz! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
    else:
        await message.answer("😉 Siz allaqachon ro'yxatdan o'tgansiz.")

    # ✅ Kanalga obuna bo‘lganini tekshirish
    if not await is_user_subscribed(message.bot, telegram_id):
        subscribe_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga a’zo bo‘lish",
                    url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ A'zo bo‘ldim",
                    callback_data="check_subscribe"
                )
            ]
        ])
        await message.answer(
            f"👋 Botdan foydalanish uchun kanalga a'zo bo‘ling.\n\n"
            f"A'zo bo‘lganingizdan so‘ng, quyidagi tugmadan foydalaning 👇",
            parse_mode="HTML",
            reply_markup=subscribe_keyboard
        )
        return

    # 📍 Asosiy menyu ko‘rsatish
    await message.answer("""📚 Taklif qilish tanlovi boshlandi!
Do‘stlaringizni taklif qiling va sovrinli kitoblardan birini yutib oling!"
🎁 Sovrinlar:
🥇 1-o‘rin: 15 ta kitobdan 2 tasini ixtiyoriy tanlab oladi
🥈 2-o‘rin: 15 ta kitobdan 1 tasini ixtiyoriy tanlab oladi
🥉 3-o‘rin: Aynan bitta aniq kitob sovg‘a qilinadi
⏳ Tanlov muddati: 15.08.2025
🔗 Har bir foydalanuvchiga shaxsiy taklif havolasi beriladi. Har bir taklif orqali kanalga qo‘shilgan odam uchun ball yig‘iladi.""",
                         reply_markup=main_menu)


@router.callback_query(F.data == "check_subscribe")
async def recheck_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id

    if await is_user_subscribed(callback.bot, user_id):
        await callback.message.edit_text("✅ A'zo bo‘lganingiz tasdiqlandi! Endi botdan to‘liq foydalanishingiz mumkin.")
        await callback.message.answer("""📚 Taklif qilish tanlovi boshlandi!
Do‘stlaringizni taklif qiling va sovrinli kitoblardan birini yutib oling!"
🎁 Sovrinlar:
🥇 1-o‘rin: 15 ta kitobdan 2 tasini ixtiyoriy tanlab oladi
🥈 2-o‘rin: 15 ta kitobdan 1 tasini ixtiyoriy tanlab oladi
🥉 3-o‘rin: Aynan bitta aniq kitob sovg‘a qilinadi
⏳ Tanlov muddati: 15.08.2025
🔗 Har bir foydalanuvchiga shaxsiy taklif havolasi beriladi. Har bir taklif orqali kanalga qo‘shilgan odam uchun ball yig‘iladi.""",
                                      reply_markup=main_menu)
    else:
        await callback.answer("❌ Siz hali ham kanalga a’zo emassiz.", show_alert=True)

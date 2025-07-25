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

            # 🔔 Taklif qilgan foydalanuvchiga bildirishnoma yuborish
            try:
                await message.bot.send_message(
                    invited_by,
                    f"📥 Siz <b>{full_name}</b> ismli foydalanuvchini taklif qildingiz!",
                    parse_mode="HTML"
                )
            except Exception as e:
                print(f"❗ Taklif qiluvchiga habar yuborib bo‘lmadi: {e}")

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
    await message.answer("""⚡️ <b>Konkurs!</b> ⚡️

😀 <b>Kitobiyat Zone</b> sahifasida <u>katta kitob sovgʻalari</u>!

🏆 <b>Sovgʻalar:</b>
🥇 <b>1-o‘rin</b> – <i>Istalgan 2 ta kitob</i>  
🥈 <b>2-o‘rin</b> – <i>Istalgan 1 ta kitob</i>  
🥉 <b>3-o‘rin</b> – <i>"Qalbimdasan, Allohim"</i>  
🏅 <b>4-o‘rin</b> – <i>"Iymon va huzun"</i>  
🏅 <b>5-o‘rin</b> – <i>"Qiyomat va oxirat"</i>

🎉 <u>Yana:</u> <b>Eng yuqori 15 ishtirokchidan 1 nafari</b> <code>random</code> orqali kitob yutadi!

⏳ <b>Tanlov muddati:</b> <u>03.08.2025 | 21:00</u>

🔗 <b>Har bir foydalanuvchiga shaxsiy taklif havolasi beriladi.</b>  
👥 <i>Har bir taklif orqali kanalga qo‘shilgan odam uchun ball yig‘iladi.</i>""",
                         reply_markup=main_menu, parse_mode="HTML")


@router.callback_query(F.data == "check_subscribe")
async def recheck_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id

    if await is_user_subscribed(callback.bot, user_id):
        await callback.message.edit_text("✅ A'zo bo‘lganingiz tasdiqlandi! Endi botdan to‘liq foydalanishingiz mumkin.")
        await callback.message.answer("""⚡️ <b>Konkurs!</b> ⚡️

😀 <b>Kitobiyat Zone</b> sahifasida <u>katta kitob sovgʻalari</u>!

🏆 <b>Sovgʻalar:</b>
🥇 <b>1-o‘rin</b> – <i>Istalgan 2 ta kitob</i>  
🥈 <b>2-o‘rin</b> – <i>Istalgan 1 ta kitob</i>  
🥉 <b>3-o‘rin</b> – <i>"Qalbimdasan, Allohim"</i>  
🏅 <b>4-o‘rin</b> – <i>"Iymon va huzun"</i>  
🏅 <b>5-o‘rin</b> – <i>"Qiyomat va oxirat"</i>

🎉 <u>Yana:</u> <b>Eng yuqori 15 ishtirokchidan 1 nafari</b> <code>random</code> orqali kitob yutadi!

⏳ <b>Tanlov muddati:</b> <u>03.08.2025 | 21:00</u>

🔗 <b>Har bir foydalanuvchiga shaxsiy taklif havolasi beriladi.</b>  
👥 <i>Har bir taklif orqali kanalga qo‘shilgan odam uchun ball yig‘iladi.</i>""",
                                      reply_markup=main_menu, parse_mode="HTML")
    else:
        await callback.answer("❌ Siz hali ham kanalga a’zo emassiz.", show_alert=True)

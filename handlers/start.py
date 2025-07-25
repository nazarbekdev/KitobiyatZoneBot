from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, CommandObject
from aiogram.exceptions import TelegramBadRequest

from database.db import db
from database import queries
from keyboards.default import main_menu

router = Router()

# Bu yerda bir nechta majburiy kanallarni ro'yxat shaklida belgilang
CHANNELS = [
    "@kitobiyat_zone",
    "@shaxsiy_satrlari"
]


async def is_user_subscribed_to_all(bot, user_id: int) -> bool:
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except TelegramBadRequest:
            return False
    return True


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    i = 1
    # Har bir kanal uchun alohida tugma qo‘shamiz
    for channel in CHANNELS:

        buttons.append([
            InlineKeyboardButton(
                text=f"📢 {i}-KANAL",
                url=f"https://t.me/{channel.lstrip('@')}"
            )
        ])
        i += 1

    # "A’zo bo‘ldim" tugmasi
    buttons.append([
        InlineKeyboardButton(
            text="✅ A'zo bo‘ldim",
            callback_data="check_subscribe"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(CommandStart(deep_link=True))
@router.message(CommandStart())
async def start_handler(message: Message, command: CommandObject):
    user = message.from_user
    telegram_id = user.id
    full_name = user.full_name
    username = user.username or ""

    referrer_id = command.args

    existing_user = db.fetchone(queries.GET_USER_BY_TELEGRAM_ID, (telegram_id,))

    if not existing_user:
        invited_by = int(referrer_id) if referrer_id and referrer_id.isdigit() and int(referrer_id) != telegram_id else None

        db.execute(
            queries.REGISTER_USER,
            (telegram_id, full_name, username, invited_by)
        )

        if invited_by:
            db.execute(queries.INCREMENT_INVITE_COUNT, (invited_by,))
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

    if not await is_user_subscribed_to_all(message.bot, telegram_id):
        await message.answer(
            "👋 Botdan foydalanish uchun quyidagi kanallarga a'zo bo‘ling!\n\n"
            "A’zo bo‘lganingizdan so‘ng pastdagi tugmadan foydalaning 👇",
            reply_markup=get_subscription_keyboard()
        )
        return

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

    if await is_user_subscribed_to_all(callback.bot, user_id):
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
        await callback.answer("❌ Siz hali ham barcha kanallarga a’zo emassiz.", show_alert=True)

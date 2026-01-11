from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton,
    InputMediaPhoto
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

# =========================
# SOZLAMALAR
# =========================

TOKEN = "8225625567:AAH7MDUwla9HjNfVbCvLPLT4yCvVqPW3np4"

ADMIN_ID = 1787954213
GROUP_ID = -1003618907297
PROOF_CHANNEL_ID = -1002547753187

CONTACT_NUMBER = "+998 91 772 03 21"  # telefon raqam
card_number = "8600 1234 5678 9012"   # admin /setcard bilan o'zgartiradi
ISM = "Sirojiddin S"

# =========================
# GLOBAL O'ZGARUVCHILAR
# =========================

user_data = {}
support_sessions = {}
last_receipts = {}
awaiting_reviews = set()
all_users = set()

BACK_BUTTON = [["⬅️ Orqaga"]]

# =========================
# MATNLAR
# =========================

UC_TEXT = """
🔥 PUBG UC TARIFLAR 🔥

60 UC  = 11 500 so'm
120 UC = 21 000 so'm
180 UC = 34 500 so'm
325 UC = 54 500 so'm
660 UC = 108 500 so'm
840 UC = 141 500 so'm
985 UC = 166 500 so'm
1800 UC = 265 500 so'm
1920 UC = 285 500 so'm
3120 UC = 480 500 so'm
3850 UC = 530 500 so'm
5650 UC = 815 500 so'm
8100 UC = 1 064 500 so'm

👇 Kerakli UC paketni tanlang:
"""

UC_PACKAGES = [
    "60 UC", "120 UC", "180 UC", "325 UC",
    "660 UC", "840 UC", "985 UC", "1800 UC",
    "1920 UC", "3120 UC", "3850 UC", "5650 UC", "8100 UC"
]

PP_TEXT = """
PP BATTLE

⚡️ ARZON PP SOTAMIZ ⚡️

🔥 10K PP - 13 000 so'm
🔥 20K PP - 26 000 so'm
🔥 30K PP - 39 000 so'm
🔥 40K PP - 52 000 so'm
⭐️ 50K PP - 65 000 so'm
🔥 70K PP - 91 000 so'm
🔥 100K PP - 130 000 so'm
⭐️ VERTALYOT - 170 000 so'm

👇 Kerakli PP paketni tanlang:
"""

PP_PACKAGES = ["10K PP", "20K PP", "30K PP", "40K PP", "50K PP", "70K PP", "100K PP", "VERTALYOT"]

PRIME_TEXT = """
👑 PRIME va PRIME PLUS obunalarini skidka narxlarda harid qilishingiz mumkin.
— Barchasi ID orqali olinadi! ✅ Akkauntga kirilmaydi ❌

✨ PRIME PLUS
1 oylik - 125 000 so'm
6 oylik - 650 000 so'm
12 oylik - 1 250 000 so'm

✨ PRIME
1 oylik - 18 000 so'm
6 oylik - 80 000 so'm
12 oylik - 145 000 so'm

👇 Kerakli xizmatni tanlang:
"""

PRIME_PACKAGES = [
    "PRIME 1 oy", "PRIME 6 oy", "PRIME 12 oy",
    "PRIME PLUS 1 oy", "PRIME PLUS 6 oy", "PRIME PLUS 12 oy"
]

# =========================
# YORDAMCHI FUNKSIYALAR
# =========================

async def send_main_menu(context, user_id):
    keyboard = [
        ["🎮 UC xizmati", "👑 PP xizmati"],
        ["⭐ PRIME / PRIME PLUS", "💼 PP sotib olamiz"]
    ]

    text = (
        "❗ Ishonmaganlar uchun 👇\n"
        f"📞 Telefon: {CONTACT_NUMBER}\n\n"
        "🏠 Bosh menyu:\n"
        "Kerakli xizmatni tanlang 👇"
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    all_users.add(user_id)
    user_data[user_id] = {"step": "service"}
    await send_main_menu(context, user_id)

# =========================
# XIZMAT OQIMLARI
# =========================

async def start_uc_flow(update, context):
    keyboard = [UC_PACKAGES[i:i+2] for i in range(0, len(UC_PACKAGES), 2)]
    await update.message.reply_text(
        UC_TEXT,
        reply_markup=ReplyKeyboardMarkup(keyboard + BACK_BUTTON, resize_keyboard=True)
    )
    user_data[update.message.from_user.id]["step"] = "uc_package"

async def start_pp_flow(update, context):
    keyboard = [PP_PACKAGES[i:i+2] for i in range(0, len(PP_PACKAGES), 2)]
    await update.message.reply_text(
        PP_TEXT,
        reply_markup=ReplyKeyboardMarkup(keyboard + BACK_BUTTON, resize_keyboard=True)
    )
    user_data[update.message.from_user.id]["step"] = "pp_package"

async def start_prime_flow(update, context):
    keyboard = [PRIME_PACKAGES[i:i+2] for i in range(0, len(PRIME_PACKAGES), 2)]
    await update.message.reply_text(
        PRIME_TEXT,
        reply_markup=ReplyKeyboardMarkup(keyboard + BACK_BUTTON, resize_keyboard=True)
    )
    user_data[update.message.from_user.id]["step"] = "prime_package"

# =========================
# ASOSIY HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    all_users.add(user_id)
    text = update.message.text

    if user_id not in user_data:
        user_data[user_id] = {}

    # ⬅️ ORQAGA
    if text == "⬅️ Orqaga":
        user_data[user_id] = {"step": "service"}
        await send_main_menu(context, user_id)
        return

    # ATZIV (yozma)
    if user_id in awaiting_reviews:
        username = f"@{update.message.from_user.username}" if update.message.from_user.username else update.message.from_user.full_name
        order = user_data.get(user_id, {})
        service = order.get("service", "Noma'lum")
        package = order.get("package", "Noma'lum")

        await context.bot.send_message(
            chat_id=PROOF_CHANNEL_ID,
            text=(
                "📝 BUYURTMACHI OTZIVI\n\n"
                f"👤 Mijoz: {username}\n"
                f"🛒 Xizmat: {service}\n"
                f"📦 Paket: {package}\n\n"
                f"💬 Fikr:\n{text}"
            )
        )

        awaiting_reviews.remove(user_id)
        await update.message.reply_text("🙏 Rahmat, fikringiz qabul qilindi!")
        await send_main_menu(context, user_id)
        return

    # SUPPORT rejim
    if user_id in support_sessions:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 SUPPORT XABAR\nUser ID: {user_id}\n\n{text}"
        )
        await update.message.reply_text("📨 Xabaringiz adminga yuborildi.")
        return

    # Xizmat tanlash
    if user_data[user_id].get("step") == "service":
        if text == "🎮 UC xizmati":
            user_data[user_id]["service"] = "UC"
            await start_uc_flow(update, context)
            return

        elif text == "👑 PP xizmati":
            user_data[user_id]["service"] = "PP"
            await start_pp_flow(update, context)
            return

        elif text == "⭐ PRIME / PRIME PLUS":
            user_data[user_id]["service"] = "PRIME"
            await start_prime_flow(update, context)
            return

        elif text == "💼 PP sotib olamiz":
            await update.message.reply_text(
                "💼 PP sotib olamiz xizmati\n\n"
                "Agar sizda PP bo‘lsa, iltimos adminga murojaat qiling:\n👉 @X_NovaUc"
            )
            return

    # UC paket
    if user_data[user_id].get("step") == "uc_package":
        if text in UC_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # PP paket
    if user_data[user_id].get("step") == "pp_package":
        if text in PP_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # PRIME paket
    if user_data[user_id].get("step") == "prime_package":
        if text in PRIME_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # ID kiritish
    if user_data[user_id].get("step") == "id":
        user_data[user_id]["player_id"] = text
        user_data[user_id]["step"] = "payment"
        await update.message.reply_text(
            f"🧾 Buyurtma:\n"
            f"Xizmat: {user_data[user_id].get('service')}\n"
            f"Paket: {user_data[user_id].get('package')}\n"
            f"ID: {text}\n\n"
            f"💳 Karta: {card_number}\nIsm: {ISM}\n\n"
            "To‘lovdan keyin chek (screenshot) yuboring."
        )
        return

# =========================
# CHEK QABUL QILISH + ATZIV RASM
# =========================

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    all_users.add(user_id)

    # ATZIV (rasm) — xizmat + paket + chek bilan
    if user_id in awaiting_reviews:
        username = f"@{update.message.from_user.username}" if update.message.from_user.username else update.message.from_user.full_name
        order = user_data.get(user_id, {})
        service = order.get("service", "Noma'lum")
        package = order.get("package", "Noma'lum")
        receipt_photo = last_receipts.get(user_id)

        caption = (
            "📝 BUYURTMACHI OTZIVI (RASM)\n\n"
            f"👤 Mijoz: {username}\n"
            f"🛒 Xizmat: {service}\n"
            f"📦 Paket: {package}\n"
        )

        if receipt_photo:
            await context.bot.send_media_group(
                chat_id=PROOF_CHANNEL_ID,
                media=[
                    InputMediaPhoto(media=update.message.photo[-1].file_id, caption=caption),
                    InputMediaPhoto(media=receipt_photo, caption="🧾 To‘lov cheki")
                ]
            )
        else:
            await context.bot.send_photo(
                chat_id=PROOF_CHANNEL_ID,
                photo=update.message.photo[-1].file_id,
                caption=caption
            )

        awaiting_reviews.remove(user_id)
        await update.message.reply_text("🙏 Rahmat, atzivingiz qabul qilindi!")
        await send_main_menu(context, user_id)
        return

    # CHEK
    if user_id in user_data and user_data[user_id].get("step") == "payment":
        order = user_data[user_id]

        caption = (
            f"🆕 YANGI BUYURTMA\n\n"
            f"Xizmat: {order.get('service')}\n"
            f"Paket: {order.get('package')}\n"
            f"ID: `{order.get('player_id')}`\n"
            f"User: {update.message.from_user.full_name}\n"
            f"TG ID: {user_id}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Bajarildi", callback_data=f"done_{user_id}"),
                InlineKeyboardButton("❌ Soxta", callback_data=f"fake_{user_id}")
            ]
        ])

        last_receipts[user_id] = update.message.photo[-1].file_id

        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=keyboard
        )

        await update.message.reply_text("✅ Chek qabul qilindi, tekshirilmoqda...")
        user_data[user_id]["step"] = "waiting"

# =========================
# ADMIN TUGMALARI
# =========================

async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.answer("Faqat admin!", show_alert=True)
        return

    data = query.data
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)

    if action == "done":
        order = user_data.get(target_user_id, {})
        service = order.get("service", "Noma'lum")
        package = order.get("package", "Noma'lum")
        player_id = order.get("player_id", "Noma'lum")

        user = await context.bot.get_chat(target_user_id)
        username = f"@{user.username}" if user.username else user.full_name

        receipt_photo = last_receipts.get(target_user_id)

        # Userga xabar + atziv so‘rash
        await context.bot.send_message(
            chat_id=target_user_id,
            text="✅ Buyurtmangiz bajarildi! Rahmat.\n\nIltimos, xizmatimiz haqida fikringizni (yozma yoki rasm) yuboring 🙏"
        )

        # Kanalga proof (chek bilan)
        proof_caption = (
            "🎉 BUYURTMA MUVAFFAQIYATLI BAJARILDI!\n\n"
            f"🛒 Xizmat: {service}\n"
            f"📦 Paket: {package}\n"
            f"🆔 ID: `{player_id}`\n"
            f"👤 Mijoz: {username}\n\n"
            "✅ Ishonchli va tez yetkazib berildi"
        )

        if receipt_photo:
            await context.bot.send_photo(
                chat_id=PROOF_CHANNEL_ID,
                photo=receipt_photo,
                caption=proof_caption,
                parse_mode="Markdown"
            )
        else:
            await context.bot.send_message(
                chat_id=PROOF_CHANNEL_ID,
                text=proof_caption,
                parse_mode="Markdown"
            )

        awaiting_reviews.add(target_user_id)

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n✔️ BAJARILDI",
            reply_markup=None
        )

    elif action == "fake":
        support_sessions[target_user_id] = ADMIN_ID
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ Chekingiz soxtaga o‘xshaydi.\nIltimos, shu yerga yozing – support tekshiradi."
        )

        await query.edit_message_caption(
            caption=query.message.caption + "\n\n❌ SOXTA - SUPPORT",
            reply_markup=None
        )

# =========================
# ADMIN REPLY → USER (SUPPORT)
# =========================

async def admin_support_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return
    if not update.message.reply_to_message:
        return

    original_text = update.message.reply_to_message.text
    if "User ID:" not in original_text:
        return

    try:
        target_user_id = int(original_text.split("User ID:")[1].split("\n")[0].strip())
        await context.bot.send_message(
            chat_id=target_user_id,
            text=f"👨‍💼 Admin:\n\n{update.message.text}"
        )
        await update.message.reply_text("✅ Userga yuborildi.")
    except:
        pass

# =========================
# SUPPORT YOPISH
# =========================

async def close_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        if user_id in support_sessions:
            del support_sessions[user_id]
            await context.bot.send_message(chat_id=user_id, text="🔒 Support yopildi.")
            await send_main_menu(context, user_id)
            await update.message.reply_text(f"🔒 Yopildi: {user_id}")
    except:
        await update.message.reply_text("❌ Format: /close USER_ID")

# =========================
# KARTA O'ZGARTIRISH (ADMIN)
# =========================

async def set_card(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global card_number

    if update.message.from_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("❌ Format: /setcard 8600 1234 5678 9012")
        return

    card_number = " ".join(context.args)
    await update.message.reply_text(f"✅ Karta raqami yangilandi:\n💳 {card_number}")

# =========================
# KUNLIK REMINDER
# =========================

async def daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Salom!\nBotdan foydalanish uchun /start bosing 🚀"
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
        except:
            pass

# =========================
# MAIN
# =========================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("close", close_support))
    app.add_handler(CommandHandler("setcard", set_card))

    app.add_handler(CallbackQueryHandler(admin_callback))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_support_reply))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Kunlik reminder ishga tushadi
    job_queue = app.job_queue
    job_queue.run_repeating(daily_reminder, interval=86400, first=10)

    app.run_polling()

if __name__ == "__main__":
    main()


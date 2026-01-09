import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8225625567:AAH7MDUwla9HjNfVbCvLPLT4yCvVqPW3np4"
ADMIN_ID = 1787954213  # o'zingning Telegram ID
GROUP_ID = -1003618907297  # buyurtmalar tushadigan group ID
KARTA = "8600 1234 5678 9012"
ISM = "Sirojiddin S"

user_data = {}
support_sessions = {}

# =========================
# UC
# =========================
UC_TEXT = """
🔥 PUBG UC TARIFLAR 🔥

60 UC  = 11 500 so'm
120 UC = 21 000 so'm
180 UC = 34 500 so'm
325 UC = 53 000 so'm
660 UC = 108 000 so'm
840 UC = 141 000 so'm
985 UC = 166 000 so'm
1800 UC = 265 000 so'm
1920 UC = 285 000 so'm
3120 UC = 480 000 so'm
3850 UC = 530 000 so'm
5650 UC = 815 500 so'm
8100 UC = 1 060 000 so'm

👇 Kerakli UC paketni tanlang:
"""

UC_PACKAGES = [
    "60 UC", "120 UC",
    "180 UC", "325 UC",
    "660 UC", "840 UC",
    "985 UC", "1800 UC",
    "1920 UC", "3120 UC",
    "3850 UC", "5650 UC",
    "8100 UC"
]

# =========================
# PP BATTLE
# =========================
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

PP_PACKAGES = [
    "10K PP", "20K PP",
    "30K PP", "40K PP",
    "50K PP", "70K PP",
    "100K PP", "VERTALYOT"
]

# =========================
# PRIME
# =========================
PRIME_TEXT = """
👑 PRIME va PRIME PLUS obunalarini skidka narxlarda harid qilishingiz mumkin.

✨ PRIME PLUS
1 oy - 125 000 so'm
6 oy - 650 000 so'm
12 oy - 1 250 000 so'm

✨ PRIME
1 oy - 18 000 so'm
6 oy - 80 000 so'm
12 oy - 145 000 so'm

👇 Kerakli xizmatni tanlang:
"""

PRIME_PACKAGES = [
    "PRIME 1 oy", "PRIME 6 oy", "PRIME 12 oy",
    "PRIME PLUS 1 oy", "PRIME PLUS 6 oy", "PRIME PLUS 12 oy"
]

# =========================
# START
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🎮 UC xizmati", "👑 PP xizmati"],
        ["⭐ PRIME / PRIME PLUS", "💼 PP sotib olamiz"]
    ]
    await update.message.reply_text(
        "Assalomu alaykum!\nQaysi xizmat kerak?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    user_data[update.message.from_user.id] = {"step": "service"}

# =========================
# FLOWS
# =========================
async def start_uc_flow(update, context):
    keyboard = [UC_PACKAGES[i:i+2] for i in range(0, len(UC_PACKAGES), 2)]
    await update.message.reply_text(UC_TEXT, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    user_data[update.message.from_user.id]["step"] = "uc_package"

async def start_pp_flow(update, context):
    keyboard = [PP_PACKAGES[i:i+2] for i in range(0, len(PP_PACKAGES), 2)]
    await update.message.reply_text(PP_TEXT, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    user_data[update.message.from_user.id]["step"] = "pp_package"

async def start_prime_flow(update, context):
    keyboard = [PRIME_PACKAGES[i:i+2] for i in range(0, len(PRIME_PACKAGES), 2)]
    await update.message.reply_text(PRIME_TEXT, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
    user_data[update.message.from_user.id]["step"] = "prime_package"

# =========================
# MAIN HANDLER
# =========================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    # SUPPORT MODE
    if user_id in support_sessions:
        admin_id = support_sessions[user_id]
        await context.bot.send_message(
            chat_id=admin_id,
            text=f"📩 SUPPORT xabar\nUser ID: {user_id}\n\n{text}"
        )
        await update.message.reply_text("📨 Xabaringiz supportga yuborildi.")
        return

    # SERVICE SELECT
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
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👨‍💼 Admin bilan bog‘lanish", url="https://t.me/X_NovaUc")]
            ])
            await update.message.reply_text(
                "💼 PP sotib olamiz xizmati\n\nAgar sizda PP bo‘lsa, adminga murojaat qiling:",
                reply_markup=keyboard
            )
            return

    # UC
    if user_data[user_id].get("step") == "uc_package":
        if text in UC_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # PP
    if user_data[user_id].get("step") == "pp_package":
        if text in PP_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # PRIME
    if user_data[user_id].get("step") == "prime_package":
        if text in PRIME_PACKAGES:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        return

    # ID
    if user_data[user_id].get("step") == "id":
        user_data[user_id]["player_id"] = text
        user_data[user_id]["step"] = "payment"
        await update.message.reply_text(
            f"🧾 Buyurtma:\n"
            f"Xizmat: {user_data[user_id].get('service')}\n"
            f"Paket: {user_data[user_id].get('package')}\n"
            f"ID: {text}\n\n"
            f"💳 Karta: {KARTA}\nIsm: {ISM}\n\n"
            "To‘lovdan keyin chek yuboring."
        )
        return

# =========================
# PHOTO (CHEK)
# =========================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and user_data[user_id].get("step") == "payment":
        order = user_data[user_id]

        caption = (
            f"🆕 YANGI BUYURTMA\n\n"
            f"Xizmat: {order.get('service')}\n"
            f"Paket: {order.get('package')}\n"
            f"ID: {order.get('player_id')}\n"
            f"User: {update.message.from_user.full_name}\n"
            f"TG ID: {user_id}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Bajarildi", callback_data=f"done_{user_id}"),
                InlineKeyboardButton("❌ Soxta", callback_data=f"fake_{user_id}")
            ]
        ])

        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            reply_markup=keyboard
        )

        await update.message.reply_text("✅ Chek qabul qilindi, tekshirilmoqda...")
        user_data[user_id]["step"] = "waiting"

# =========================
# ADMIN CALLBACK
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
        await context.bot.send_message(
            chat_id=target_user_id,
            text="✅ Buyurtmangiz bajarildi. Rahmat!"
        )
        await query.edit_message_caption(query.message.caption + "\n\n✔️ BAJARILDI", reply_markup=None)
        if target_user_id in user_data:
            del user_data[target_user_id]

    elif action == "fake":
        support_sessions[target_user_id] = ADMIN_ID
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ Chekingiz soxtaga o‘xshaydi.\nSupport bilan bog‘laning, shu yerga yozing."
        )
        await query.edit_message_caption(query.message.caption + "\n\n❌ SOXTA - SUPPORT", reply_markup=None)

# =========================
# ADMIN REPLY SUPPORT
# =========================
async def admin_support_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original = update.message.reply_to_message.text
        if "User ID:" in original:
            try:
                target_user_id = int(original.split("User ID:")[1].split("\n")[0].strip())
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"👨‍💼 Admin:\n\n{update.message.text}"
                )
                await update.message.reply_text("✅ Userga yuborildi.")
            except:
                pass

# =========================
# CLOSE SUPPORT
# =========================
async def close_support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        if user_id in support_sessions:
            del support_sessions[user_id]
            await update.message.reply_text(f"🔒 Support yopildi: {user_id}")
            await context.bot.send_message(
                chat_id=user_id,
                text="🔒 Support yopildi. /start bosing."
            )
    except:
        await update.message.reply_text("❌ Format: /close USER_ID")

# =========================
# MAIN
# =========================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("close", close_support))
    app.add_handler(CallbackQueryHandler(admin_callback))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, admin_support_reply))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()


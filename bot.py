import asyncio
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8225625567:AAH7MDUwla9HjNfVbCvLPLT4yCvVqPW3np4"
ADMIN_ID = 6058698891  # o'zingning Telegram ID
GROUP_ID = -5217526899  # buyurtmalar tushadigan group ID
KARTA = "5614 6846 0189 1797"
ISM = "Sirojiddin S"

user_data = {}

TARIFS_TEXT = """
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
"""

TARIFS = [
    "60 UC", "120 UC", "180 UC", "325 UC", "660 UC",
    "840 UC", "985 UC", "1800 UC", "1920 UC", "3120 UC",
    "3850 UC", "5650 UC", "8100 UC"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [TARIFS[i:i+2] for i in range(0, len(TARIFS), 2)]
    await update.message.reply_text(
        TARIFS_TEXT + "\n👇 Kerakli UC paketni tanlang:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )
    user_data[update.message.from_user.id] = {"step": "package"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # 1. Paket tanlash
    if user_id in user_data and user_data[user_id]["step"] == "package":
        if text in TARIFS:
            user_data[user_id]["package"] = text
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 PUBG Player ID ni kiriting:")
        else:
            await update.message.reply_text("❌ Pastdagi tugmalardan birini tanlang.")

    # 2. ID kiritildi
    elif user_id in user_data and user_data[user_id]["step"] == "id":
        user_data[user_id]["player_id"] = text
        user_data[user_id]["step"] = "confirm"
        keyboard = [["✅ To‘g‘ri", "✏️ Tahrirlash"]]
        await update.message.reply_text(
            f"🆔 Kiritilgan ID: {text}\n\nTo‘g‘rimi?",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    # 3. Tasdiqlash yoki tahrirlash
    elif user_id in user_data and user_data[user_id]["step"] == "confirm":
        if text == "✅ To‘g‘ri":
            user_data[user_id]["step"] = "payment_wait"
            await update.message.reply_text(
                f"🧾 Buyurtma:\n"
                f"📦 Paket: {user_data[user_id]['package']}\n"
                f"🆔 ID: {user_data[user_id]['player_id']}\n\n"
                f"💳 To‘lov uchun karta:\n{KARTA}\nIsm: {ISM}\n\n"
                "To‘lovni amalga oshiring..."
            )
            await asyncio.sleep(30)
            if user_id in user_data and user_data[user_id]["step"] == "payment_wait":
                user_data[user_id]["step"] = "payment"
                await update.message.reply_text("📸 Endi chek (screenshot) yuboring:")

        elif text == "✏️ Tahrirlash":
            user_data[user_id]["step"] = "id"
            await update.message.reply_text("🆔 Player ID ni qayta kiriting:")

        else:
            await update.message.reply_text("Iltimos, tugmalardan foydalaning.")

    else:
        await update.message.reply_text("Boshlash uchun /start bosing.")

# 4. Chek qabul qilish va groupga tashlash
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_data and user_data[user_id]["step"] == "payment":
        order = user_data[user_id]

        caption = (
            f"🆕 YANGI BUYURTMA\n\n"
            f"👤 User: {update.message.from_user.full_name}\n"
            f"🆔 ID: {order['player_id']}\n"
            f"📦 Paket: {order['package']}\n"
            f"TG ID: {user_id}"
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ UC ishonchli tushirildi", callback_data=f"done_{user_id}"),
                InlineKeyboardButton("❌ Chek soxtaga o‘xshaydi", callback_data=f"fake_{user_id}")
            ]
        ])

        await context.bot.send_photo(
            chat_id=GROUP_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            reply_markup=keyboard
        )

        await update.message.reply_text("✅ Chek qabul qilindi. Tekshirilmoqda...")
        user_data[user_id]["step"] = "waiting_admin"

# 5. Admin tugmalarini ishlatish
async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.answer("Faqat admin bosishi mumkin!", show_alert=True)
        return

    data = query.data  # done_12345 yoki fake_12345
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)

    if action == "done":
        await context.bot.send_message(
            chat_id=target_user_id,
            text="✅ UC ishonchli va tez tushirildi! Rahmat, yana murojaat qiling."
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n✔️ BAJARILDI")
    elif action == "fake":
        await context.bot.send_message(
            chat_id=target_user_id,
            text="❌ Chekingiz soxtaga o‘xshaydi. Iltimos, to‘g‘ri chek yuboring."
        )
        await query.edit_message_caption(caption=query.message.caption + "\n\n❌ SOXTA CHEK")

    # Tugmalarni o‘chiramiz
    await query.edit_message_reply_markup(reply_markup=None)

    if target_user_id in user_data:
        del user_data[target_user_id]

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(admin_callback))
    app.run_polling()

if __name__ == "__main__":
    main()


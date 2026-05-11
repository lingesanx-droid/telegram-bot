from flask import Flask
from threading import Thread
import os
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running!"

def run():
    app_web.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 10000))
    )

Thread(target=run).start()

TOKEN = "8719992437:AAF-Yz2YT2gpRhS7oN2CgO8i2ieVb2_Om9Y"

VIDEOS = [
    "BAACAgUAAxkBAAFJVglqAbv6GE6TgqlZF8B7XqSzAAGL9XAAAuAeAAL3LglUZ0eCl43OUeE7BA",
    "BAACAgUAAxkBAAFJVgpqAbv6gA8WZmECWbeecEqcUxub2gAC4R4AAvcuCVReMdWdu4OrezsE",
    "BAACAgUAAxkBAAFJVgtqAbv6PJp17U8ZmPtAjw9UBlxBKAAC4h4AAvcuCVQfgTGrVUhbNDsE",
    "BAACAgUAAxkBAAFJVgxqAbv6vKrNs-YeC9i8omsWn8qFwgAC4x4AAvcuCVSrpuF_8WTpKjsE",
    "BAACAgUAAxkBAAFJVg1qAbv66nQ7N9ZuVrp5I7AC1IrT-QAC5B4AAvcuCVRu2LAGvDq2yTsE"
]

BUY_LINK = "https://t.me/unseenclipsbot"
PROOF_LINK = "https://t.me/unseenxproofs"
ADMIN_LINK = "https://t.me/igmikasa"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("💸 Buy Access", url=BUY_LINK)],
        [InlineKeyboardButton("📸 Payment Proofs", url=PROOF_LINK)],
        [InlineKeyboardButton("👑 Admin Contact", url=ADMIN_LINK)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = """
🔥 FREE DEMO PREVIEW 🔥

⏰ Demo auto delete in 2 minutes
💎 Buy premium access below
"""

    await update.message.reply_text(
        text,
        reply_markup=reply_markup
    )

    sent_messages = []

    for video in VIDEOS:
        msg = await context.bot.send_video(
            chat_id=update.effective_chat.id,
            video=video
        )

        sent_messages.append(msg.message_id)

    await asyncio.sleep(120)

    for msg_id in sent_messages:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=msg_id
            )
        except:
            pass

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="❌ Demo Expired\n\n💸 Buy Full Access Below",
        reply_markup=reply_markup
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot Running...")
app.run_polling()

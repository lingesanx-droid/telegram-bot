from flask import Flask
from threading import Thread

app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is running!"

def run():
    app_web.run(host='0.0.0.0', port=10000)

Thread(target=run).start()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "8719992437:AAEsq8TNcR0tkO_i0Rjhij2g6tVoeYxTwdc"

VIDEOS = []

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

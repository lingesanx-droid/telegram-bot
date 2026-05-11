from flask import Flask
from threading import Thread
import os
import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================= WEB SERVER =================

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

# ================= BOT TOKEN =================

TOKEN = "8719992437:AAF-Yz2YT2gpRhS7oN2CgO8i2ieVb2_Om9Y"

# ================= VIDEOS =================

VIDEOS = [
    "videos_1.mp4",
    "videos_2.mp4",
    "videos_3.mp4",
    "videos_4.mp4",
    "videos_5.mp4"
]

# ================= BUTTON LINKS =================

BUY_LINK = "https://t.me/unseenclipsbot"
PROOF_LINK = "https://t.me/unseenxproofs"
ADMIN_LINK = "https://t.me/igmikasa"

# ================= BUTTONS =================

keyboard = [
    [InlineKeyboardButton("💸 Buy Access", url=BUY_LINK)],
    [InlineKeyboardButton("📸 Payment Proofs", url=PROOF_LINK)],
    [InlineKeyboardButton("👑 Admin Contact", url=ADMIN_LINK)]
]

reply_markup = InlineKeyboardMarkup(keyboard)

# ================= START COMMAND =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 FREE DEMO PREVIEW 🔥

⏰ Demo auto delete in 1 minute
💎 Buy premium access below
"""

    # SEND MAIN TEXT
    main_msg = await update.message.reply_text(
        text=text,
        reply_markup=reply_markup
    )

    sent_messages = []

    # ================= SEND VIDEOS =================

    for video in VIDEOS:

        video_path = os.path.join(os.getcwd(), video)

        if os.path.exists(video_path):

            with open(video_path, "rb") as vid:

                msg = await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=vid
                )

                sent_messages.append(msg.message_id)

    # ================= WAIT 1 MINUTE =================

    await asyncio.sleep(60)

    # ================= DELETE VIDEOS =================

    for msg_id in sent_messages:
        try:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=msg_id
            )
        except:
            pass

    # ================= DELETE MAIN TEXT =================

    try:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=main_msg.message_id
        )
    except:
        pass

    # ================= FINAL BUTTONS ONLY =================

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="💸 Purchase Premium Access Below",
        reply_markup=reply_markup
    )

# ================= RUN BOT =================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("Bot Running...")

app.run_polling()

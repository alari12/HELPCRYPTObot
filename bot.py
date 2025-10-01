# bot.py
import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram.error import Forbidden, BadRequest
from dotenv import load_dotenv

# Load local .env when running locally
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get"8256075938:AAGelvhEM-0DnLCiGeJld49jc_8NWD3bTDU"
HELP_LINK = os.environ.get"HELP_LINK", "https://alari12.github.io/MindCarePLC/"
TRIGGERS = os.environ.get("TRIGGERS", "wallet,usdt,crypto,sol,help")
TRIGGER_WORDS = [t.strip().lower() for t in TRIGGERS.split(",") if t.strip()]

if not TOKEN:
    logger.error("Missing TELEGRAM_TOKEN environment variable. Exiting.")
    raise SystemExit("TELEGRAM_TOKEN is required as env var")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Use only in private chat with user
    await update.message.reply_text(
        "Hi — I'm your Wallet Help Bot. "
        " please press Start here."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Watch group messages and DM user a single help link if trigger found."""
    if update.message is None or update.message.text is None:
        return

    # ignore messages from other bots
    if update.message.from_user and update.message.from_user.is_bot:
        return

    text = update.message.text.lower()

    for word in TRIGGER_WORDS:
        if word in text:
            user = update.message.from_user
            user_id = user.id
            first = user.first_name or "there"
            dm_text = f"Hey {first}, I noticed you mentioned '{word}'. For help click: {https://alari12.github.io/MindCarePLC/}"

            try:
                # Try to DM the user
                await context.bot.send_message(chat_id=user_id, text=dm_text)
                logger.info("Sent DM to user_id=%s for trigger=%s", user_id, word)
            except Forbidden:
                # Can't DM the user (likely they haven't started a private chat).
                # Fallback: politely reply in the group telling them to start a chat with the bot
                try:
                    bot_user = await context.bot.get_me()
                    bot_username = bot_user.username or "this_bot"
                    start_link = f"https://t.me/{bot_username}"
                    fallback = (
                        f"{user.first_name or '@user'}, I tried to DM you but couldn't. "
                        f"Please start a private chat with me here so I can help: {start_link}"
                    )
                    await update.message.reply_text(fallback)
                    logger.info("Could not DM user %s — fallback message sent in group.", user_id)
                except Exception as e:
                    logger.exception("Fallback reply in group failed: %s", e)
            except BadRequest as e:
                logger.exception("Bad request when trying to DM: %s", e)
            except Exception as e:
                logger.exception("Unexpected error sending DM: %s", e)
            break  # only send once per message

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot starting — running polling.")
    app.run_polling()

if __name__ == "__main__":
    main()

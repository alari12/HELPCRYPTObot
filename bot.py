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

# Load local .env (when running locally only)
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables (✅ DO NOT put your token here)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
HELP_LINK = os.environ.get"HELP_LINK", "https://example.com/help"
TRIGGERS = os.environ.get"TRIGGERS", "wallet,usdt,crypto,sol,help"
TRIGGER_WORDS = [t.strip().lower() for t in TRIGGERS.split(",") if t.strip()]

if not TOKEN:
    logger.error("❌ Missing TELEGRAM_TOKEN environment variable. Exiting.")
    raise SystemExit("TELEGRAM_TOKEN is required as env var")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I monitor groups for crypto keywords and will DM you with help. "
        "Make sure you’ve started me in private first!"
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Here’s your help link: {HELP_LINK}")

# Monitor group messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.text is None:
        return

    if update.message.from_user and update.message.from_user.is_bot:
        return  # ignore bots

    text = update.message.text.lower()

    for word in TRIGGER_WORDS:
        if word in text:
            user = update.message.from_user
            user_id = user.id
            first = user.first_name or "there"
            dm_text = f"Hey {first}, I noticed you mentioned '{word}'. For help click: {HELP_LINK}"

            try:
                await context.bot.send_message(chat_id=user_id, text=dm_text)
                logger.info("✅ Sent DM to %s for trigger '%s'", user_id, word)
            except Forbidden:
                try:
                    bot_user = await context.bot.get_me()
                    bot_username = bot_user.username or "this_bot"
                    start_link = f"https://t.me/{bot_username}"
                    fallback = (
                        f"{user.first_name}, I tried to DM you but couldn’t. "
                        f"Please start a private chat with me here: {start_link}"
                    )
                    await update.message.reply_text(fallback)
                    logger.info("⚠️ Fallback message sent in group to %s", user_id)
                except Exception as e:
                    logger.exception("Group fallback failed: %s", e)
            except BadRequest as e:
                logger.exception("Bad request sending DM: %s", e)
            except Exception as e:
                logger.exception("Unexpected error: %s", e)
            break  # only once per message

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🚀 Bot starting…")
    app.run_polling()

if __name__ == "__main__":
    main()

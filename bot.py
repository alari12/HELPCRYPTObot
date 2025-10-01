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

# Environment variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
HELP_LINK = os.environ.get("HELP_LINK", "https://alari12.github.io/MindCarePLC/")
TRIGGERS = os.environ.get("TRIGGERS", "wallet,usdt,crypto,sol,help")
TRIGGER_WORDS = [t.strip().lower() for t in TRIGGERS.split(",") if t.strip()]

if not TOKEN:
    logger.error("❌ Missing TELEGRAM_TOKEN environment variable. Exiting.")
    raise SystemExit("TELEGRAM_TOKEN is required as env var")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome! I’m your Crypto Help Assistant.\n\n"
        "I provide quick guidance and trusted resources for your crypto needs. "
        "Type /help to get started or just mention crypto-related terms in a group."
    )

# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🤝 I’m here to assist you!\n\n"
        f"Here’s a reliable resource that can guide you further:\n{HELP_LINK}\n\n"
        "⚡ If you need more support, just reach out anytime."
    )

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
            dm_text = (
                f"Hello {first}, 👋\n\n"
                "I noticed your message and thought this might help you.\n"
                f"Here’s a trusted resource: {HELP_LINK}\n\n"
                "💡 Keep me handy — I’ll assist whenever you need support."
            )

            try:
                await context.bot.send_message(chat_id=user_id, text=dm_text)
                logger.info("✅ Sent DM to %s for trigger '%s'", user_id, word)
            except Forbidden:
                # ❌ No group fallback, just stay silent
                logger.info("⚠️ Couldn’t DM %s (Forbidden). Staying silent.", user_id)
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


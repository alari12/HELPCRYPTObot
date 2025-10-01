import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Get token from environment variable
TOKEN = os.environ.get("TELEGRAM_TOKEN")

HELP_LINK = os.environ.get"HELP_LINK", "https://alari12.github.io/MindCarePLC/"
TRIGGERS = "[wallet" , "usdt","crypto","sol","help"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Type any of the trigger words to get assistance.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(word in text for word in TRIGGERS):
        await context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=f"Here’s a helpful link:"https://alari12.github.io/MindCarePLC/"
        )

def main():
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_TOKEN environment variable")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()

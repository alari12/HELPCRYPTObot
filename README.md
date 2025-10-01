# Telegram Wallet Helper Bot

This bot monitors group messages for trigger words and sends a private DM with a help link.

## Setup
1. Copy `.env.example` → `.env` and fill values (do not commit `.env`).
2. Install requirements: `pip install -r requirements.txt`
3. Run locally: `python bot.py`

## Deploy
- Recommended: use Railway (see instructions in project wiki or follow the guide in the README).

## Notes
- Make sure to disable Bot Privacy Mode in @BotFather or make the bot an admin so it sees group messages.
- Users must start a private chat with the bot for it to DM them.

from telegram import Bot
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

bot = Bot(TELEGRAM_TOKEN)

def send_alert(msg: str):
    """
    Push a message to your Telegram smartphone.
    """
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

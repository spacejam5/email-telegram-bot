from telegram import Bot
import os

bot = Bot(token=os.environ['BOT_TOKEN'])
chat_id = int(os.environ['CHAT_ID'])
bot.send_message(chat_id=chat_id, text="✅ Бот успешно получил доступ и может отправлять сообщения!")

from telegram import Bot
import os

# Получаем переменные окружения
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])

# Создаем экземпляр бота и отправляем сообщение
bot = Bot(token=TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Бот успешно получил доступ и может отправлять сообщения!")

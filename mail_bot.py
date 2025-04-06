import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
from telegram import Bot
import os
import datetime
import html

# Настройки почты
IMAP_SERVER = 'imap.yandex.ru'
EMAIL = os.environ['EMAIL']
PASSWORD = os.environ['EMAIL_PASSWORD']

# Настройки Telegram
TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])

# Экранирование спецсимволов для Telegram HTML
def escape_html(text):
    return html.escape(text)

# Получение писем за последние сутки
def check_email():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')

        # Получаем письма, пришедшие с вчерашнего дня
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{yesterday}")')
        email_ids = messages[0].split()

        new_emails = []

        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # Тема письма
            subject, encoding = decode_header(msg.get("Subject", ""))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            # Имя отправителя
            from_header = msg.get("From", "")
            from_name, from_email = parseaddr(from_header)
            decoded_name, enc = decode_header(from_name)[0]
            if isinstance(decoded_name, bytes):
                from_name = decoded_name.decode(enc or "utf-8", errors="ignore")
            else:
                from_name = decoded_name

            if not from_name:
                from_name = from_email

            new_emails.append((subject, from_name))

        return new_emails

# Отправка сообщений в Telegram
def send_notifications(bot, new_emails):
    for subject, from_ in new_emails:
        subject = escape_html(subject)
        from_ = escape_html(from_)
        message = f"📩 <b>Новое письмо за последние сутки</b>\n\n<b>От:</b> {from_}\n<b>Тема:</b> {subject}"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

# Главная функция
def main():
    bot = Bot(token=TOKEN)
    new_emails = check_email()
    if new_emails:
        send_notifications(bot, new_emails)

# Точка входа
if __name__ == "__main__":
    main()

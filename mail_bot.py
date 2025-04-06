import imaplib
import email
from email.header import decode_header
from telegram import Bot
from telegram.helpers import escape_html
import os
import datetime
from telegram.helpers import escape_html

IMAP_SERVER = 'imap.yandex.ru'
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = int(os.environ.get('CHAT_ID'))

def check_email():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')

        # письма за последние сутки
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%d-%b-%Y")
        status, messages = mail.search(None, f'(SINCE "{yesterday}")')

        email_ids = messages[0].split()

        new_emails = []
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            # декодируем тему письма
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            # декодируем имя отправителя
            from_header = msg.get("From")
            from_name, from_addr = email.utils.parseaddr(from_header)
            from_name, encoding = decode_header(from_name)[0]
            if isinstance(from_name, bytes):
                from_name = from_name.decode(encoding or "utf-8")
            if not from_name:
                from_name = from_addr  # Если имени нет, используем адрес

            new_emails.append((subject, from_name))
        return new_emails


def send_notifications(bot, new_emails):
    for subject, from_ in new_emails:
        subject = escape_html(subject)
        from_ = escape_html(from_)
        message = f"📩 <b>Новое письмо за последние сутки</b>\n\n<b>От:</b> {from_}\n<b>Тема:</b> {subject}"
        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

async def main():
    bot = Bot(token=TOKEN)
    new_emails = check_email()
    for subject, from_ in new_emails:
        await send_notification(bot, subject, from_)

if __name__ == "__main__":
    asyncio.run(main())

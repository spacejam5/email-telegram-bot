import imaplib
import email
from email.header import decode_header
from telegram import Bot
import asyncio
import os

IMAP_SERVER = 'imap.yandex.ru'
EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = int(os.environ.get('CHAT_ID'))

def check_email():
    with imaplib.IMAP4_SSL(IMAP_SERVER) as mail:
        mail.login(EMAIL, PASSWORD)
        mail.select('INBOX')

        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()

        new_emails = []
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8")

            from_, encoding = decode_header(msg.get("From"))[0]
            if isinstance(from_, bytes):
                from_ = from_.decode(encoding or "utf-8")

            new_emails.append((subject, from_))
        return new_emails

async def send_notification(bot, subject, from_):
    message = f"📩 <b>Новое письмо</b>\n\n<b>От:</b> {from_}\n<b>Тема:</b> {subject}"
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='HTML')

async def main():
    bot = Bot(token=TOKEN)
    new_emails = check_email()
    for subject, from_ in new_emails:
        await send_notification(bot, subject, from_)

if __name__ == "__main__":
    asyncio.run(main())

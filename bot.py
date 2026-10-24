import os
import re
import logging
from urllib.parse import urlparse

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
Application,
CommandHandler,
MessageHandler,
CallbackQueryHandler,
ContextTypes,
filters,
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv(“TELEGRAM_BOT_TOKEN”)
CHANNEL = os.getenv(“TELEGRAM_CHANNEL”, “@realtyhelpuz”)
PHONE = os.getenv(“CONTACT_PHONE”, “+998 97 446 88 11”)
CONTACT_NAME = os.getenv(“CONTACT_NAME”, “Muhammad”)

def valid_olx_url(text):
try:
u = urlparse(text.strip())
return u.scheme in (“http”, “https”) and (
u.netloc.endswith(“olx.uz”) or u.netloc.endswith(“www.olx.uz”)
)
except Exception:
return False

def format_post(url, title, description, price):
return (
f”🏠 {title or ‘Sotiladi · Ko‘chmas mulk’}\n\n”
f”{description or ‘Tafsilotlar e’lon havolasida.’}\n\n”
f”💰 Narxi: {price or ‘Kelishiladi’}\n”
f”📞 Murojaat: {PHONE} ({CONTACT_NAME})\n\n”
f”🔗 OLX e’loni: {url}\n\n”
“#Toshkent #Kvartira #Ko‘chmasMulk #sotuv”
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
“Assalomu alaykum! OLX.uz e’lon havolasini yuboring. “
“Men uni kanal uchun tayyorlab beraman.”
)

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text.strip()
if not valid_olx_url(url):
await update.message.reply_text(
“Iltimos, olx.uz saytidagi e’lonning to‘liq havolasini yuboring.”
)
return

await update.message.reply_text(
    "Havola qabul qilindi. Hozircha e’lon ma’lumotlarini avtomatik "
    "o‘qish funksiyasi ulanmagan. Keyingi bosqichda OLX brauzerini ulaymiz.\n\n"
    f"Havola: {url}"
)

async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
await query.edit_message_text(
“Kanalga joylash funksiyasi keyingi bosqichda ulanadi.”
)

def main():
if not TOKEN:
raise RuntimeError(“TELEGRAM_BOT_TOKEN Render sozlamalarida kiritilmagan.”)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
app.add_handler(CallbackQueryHandler(publish))
app.run_polling()

if name == “main”:
main()

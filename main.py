from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import re

TOKEN = "7881203153:AAHO-jtkBBPSWNagptJEgNhk5B9M6-Xa9oQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک استوری اینستاگرام رو بفرست تا منشن‌شده‌هاشو پیدا کنم.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        mentions = re.findall(r'"ig_mention":\s*{[^}]*"username":"([^"]+)"', html)
        if mentions:
            text = "🧾 کاربران منشن‌شده:\n" + "\n".join(f"@{u}" for u in mentions)
        else:
            text = "❗ منشن‌ای پیدا نکردم. شاید لینک اشتباهه یا استوری private باشه."
    except Exception as e:
        text = "⚠️ خطا: " + str(e)
    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
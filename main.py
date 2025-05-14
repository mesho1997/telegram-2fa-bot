import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ضع التوكن الخاص بك هنا
BOT_TOKEN = '7650750210:AAFzjgFg_sTR7fSXQW2hc-_e3NcXlYkbWII'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل المفتاح السري هكذا:\n/code ABCDEFGHIJKL")

async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ رجاءً أرسل المفتاح السري بعد الأمر.\nمثال: /code ABCDEFGHIJKL")
        return

    secret = context.args[0]
    try:
        response = requests.get(f"https://2fa.live/tok/{secret}")
        data = response.json()
        token = data.get("token")
        if token:
            await update.message.reply_text(f"✅ الرمز الحالي هو:\n`{token}`", parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ لم يتم توليد الرمز. تأكد من صحة المفتاح.")
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ أثناء جلب الرمز.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("code", get_code))
app.run_polling()

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler

BOT_TOKEN = "8598067935:AAFqV8DnyN0kKHtcgZeHWCbriObQE8-Yb2I"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Xin chào!\nGửi link TikTok, mình sẽ tải video không watermark cho bạn."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" not in text:
        await update.message.reply_text("❌ Hãy gửi link TikTok.")
        return

    await update.message.reply_text("⏳ Đang tải video, vui lòng chờ...")

    try:
        api_url = "https://tikwm.com/api/"
        params = {"url": text}

        r = requests.get(api_url, params=params, timeout=15)
        data = r.json()

        video_url = data["data"]["play"]

        await update.message.reply_video(video=video_url)

    except Exception as e:
        await update.message.reply_text("⚠️ Lỗi khi tải video, thử lại sau.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🤖 Bot đang chạy...")
app.run_polling()

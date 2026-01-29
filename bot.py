import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler,
)

# =========================
# DÁN TOKEN BOT CỦA BẠN VÀO ĐÂY
# =========================
BOT_TOKEN = "8598067935:AAFqV8DnyN0kKHtcgZeHWCbriObQE8-Yb2I"


# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Xin chào!\n\n"
        "📌 Gửi link:\n"
        "• TikTok\n"
        "• Douyin (Trung Quốc)\n\n"
        "👉 Bot sẽ tải video KHÔNG watermark cho bạn."
    )


# Xử lý link video
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    await update.message.reply_text("⏳ Đang xử lý video, vui lòng chờ...")

    try:
        # ===== TikTok =====
        if "tiktok.com" in text:
            api_url = "https://tikwm.com/api/"
            r = requests.get(api_url, params={"url": text}, timeout=15)
            data = r.json()

            video_url = data["data"]["play"]

        # ===== Douyin (Trung Quốc) =====
        elif "douyin.com" in text:
            api_url = "https://www.wetools.com/api/douyin"
            r = requests.get(api_url, params={"url": text}, timeout=15)
            data = r.json()

            video_url = data["data"]["video"]["play_addr"]["url_list"][0]

        else:
            await update.message.reply_text(
                "❌ Link không hợp lệ.\n"
                "👉 Chỉ hỗ trợ TikTok và Douyin."
            )
            return

        # Gửi video về Telegram
        await update.message.reply_video(video=video_url)

    except Exception as e:
        await update.message.reply_text(
            "⚠️ Không tải được video.\n"
            "👉 Có thể link lỗi hoặc API tạm thời không hoạt động."
        )


# =========================
# KHỞI TẠO BOT
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

print("🤖 Bot đang chạy...")
app.run_polling()

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler,
    CallbackQueryHandler,
)

# ==================================================
# CẤU HÌNH
# ==================================================
BOT_TOKEN = "8598067935:AAFqV8DnyN0kKHtcgZeHWCbriObQE8-Yb2I"
OWNER_ID = 6015869726  # DÁN TELEGRAM USER ID CỦA BẠN


# ==================================================
# KIỂM TRA CHỈ CHỦ BOT
# ==================================================
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID


# ==================================================
# /start
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.message.reply_text("⛔ Bot này chỉ dùng cho cá nhân.")
        return

    await update.message.reply_text(
        "👋 Xin chào!\n\n"
        "📌 Gửi link TikTok hoặc Douyin\n"
        "👇 Sau đó chọn chức năng bằng nút bên dưới"
    )


# ==================================================
# NHẬN LINK
# ==================================================
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    url = update.message.text.strip()
    context.user_data["last_url"] = url

    keyboard = [
        [
            InlineKeyboardButton("🎬 Tải Video", callback_data="video"),
            InlineKeyboardButton("🎵 Tải Audio", callback_data="audio"),
        ]
    ]

    await update.message.reply_text(
        "👉 Bạn muốn tải gì?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ==================================================
# XỬ LÝ NÚT BẤM
# ==================================================
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_owner(update):
        return

    url = context.user_data.get("last_url")
    if not url:
        await query.message.reply_text("❌ Không tìm thấy link.")
        return

    await query.message.reply_text("⏳ Đang xử lý, vui lòng chờ...")

    try:
        # ==================================================
        # TIKTOK (API CHÍNH + DỰ PHÒNG)
        # ==================================================
        if "tiktok.com" in url:
            try:
                # API CHÍNH
                r = requests.get(
                    "https://tikwm.com/api/",
                    params={"url": url},
                    timeout=15,
                )
                data = r.json()
                video_url = data["data"]["play"]
                audio_url = data["data"]["music"]

            except:
                # API DỰ PHÒNG
                r = requests.get(
                    "https://api.tiklydown.me/api/download",
                    params={"url": url},
                    timeout=15,
                )
                data = r.json()
                video_url = data["video"]["noWatermark"]
                audio_url = data["music"]

        # ============================

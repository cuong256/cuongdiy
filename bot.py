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

# =========================
# CẤU HÌNH
# =========================
BOT_TOKEN = "8598067935:AAFqV8DnyN0kKHtcgZeHWCbriObQE8-Yb2I"
OWNER_ID = 6015869726  # DÁN TELEGRAM ID CỦA BẠN


# =========================
# KIỂM TRA QUYỀN
# =========================
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID


# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        await update.message.reply_text("⛔ Bot này chỉ dùng cho cá nhân.")
        return

    await update.message.reply_text(
        "👋 Xin chào!\n\n"
        "📌 Gửi link TikTok hoặc Douyin\n"
        "👇 Chọn chức năng bằng nút bên dưới"
    )


# =========================
# NHẬN LINK
# =========================
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    text = update.message.text.strip()
    context.user_data["last_url"] = text

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


# =========================
# XỬ LÝ NÚT BẤM
# =========================
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
        # =========================
        # TIKTOK – API CHÍNH + DỰ PHÒNG
        # =========================
        if "tiktok.com" in url:
            try:
                # API CHÍNH
                r = requests.get("https://tikwm.com/api/", params={"url": url}, timeout=10)
                data = r.json()
                video_url = data["data"]["play"]
                audio_url = data["data"]["music"]
            except:
                # API DỰ PHÒNG
                r = requests.get("https://api.tiklydown.me/api/download", params={"url": url}, timeout=10)
                data = r.json()
                video_url = data["video"]["noWatermark"]
                audio_url = data["music"]

        # =========================
        # DOUYIN – API CHÍNH + DỰ PHÒNG
        # =========================
        elif "douyin.com" in url:
            try:
                # API CHÍNH
                r = requests.get("https://www.wetools.com/api/douyin", params={"url": url}, timeout=10)
                data = r.json()
                video_url = data["data"]["video"]["play_addr"]["url_list"][0]
                audio_url = data["data"]["video"]["music"]["play_url"]["url_list"][0]
            except:
                # API DỰ PHÒNG
                r = requests.get("https://api.douyin.wtf/api", params={"url": url}, timeout=10)
                data = r.json()
                video_url = data["video"]
                audio_url = data["music"]

        else:
            await query.message.reply_text("❌ Chỉ hỗ trợ TikTok & Douyin.")
            return

        # =========================
        # GỬI KẾT QUẢ
        # =========================
        if query.data == "video":
            await query.message.reply_video(video=video_url)
        else:
            await query.message.reply_audio(audio=audio_url)

    except Exception as e:
        await query.message.reply_text("⚠️ Lỗi khi tải. Tất cả API đều không phản hồi.")


# =========================
# KHỞI TẠO BOT
# =========================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(handle_button))

print("🤖 Bot đang chạy...")
app.run_polling()

import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "8615831210:AAGNV7Wb3rSd3zNguzwFDBcXsBALR7Ul5q8")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا بك في بوت التحميل ، ارسل رابط الفديو لتحميله⭐.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        await update.message.reply_text("Please send a valid URL.")
        return
    msg = await update.message.reply_text("Downloading...")
    try:
        ydl_opts = {
            "format": "best[filesize<50M]/best",
            "outtmpl": "/tmp/%(title)s.%(ext)s",
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        await msg.edit_text("Sending...")
        with open(file_path, "rb") as video:
            await update.message.reply_video(video=video)
        os.remove(file_path)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"Error: {str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()

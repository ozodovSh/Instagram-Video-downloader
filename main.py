from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, ConversationHandler
import os
import re
import instaloader

TOKEN = ''

L = instaloader.Instaloader(
    download_comments=False,
    download_video_thumbnails=False,
    save_metadata=False,
    download_pictures=False,
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello you can install instagram reels and stories with this bot🙋‍♂️")
    return

def short_cut(url: str):
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?]+)", url)
    return match.group(1) if match else None

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "instagram.com" not in text:
        return update.message.reply_text("Wrong Instagram link!!!")

    shortcode = short_cut(text)
    if not shortcode:
        return update.message.reply_text("Wrong link!!!")

    try:
        update.message.reply_text("downloading...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target='downloads')
        for file in os.listdir('downloads'):
            if file.endswith(".mp4"):
                path = f"downloads/{file}"
                update.message.reply_video(video=open(path, "rb"))
                os.remove(path)
        update.message.reply_text("ready")

    except Exception as e:
        update.message.reply_text("404")
        print(e)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text &~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()



































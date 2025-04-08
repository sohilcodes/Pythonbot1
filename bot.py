from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
import random
import os

# Bot credentials
TOKEN = '7761085703:AAHrcbfYoKF7d38WA85w_orLl1vO_moEZ_k'
ADMIN_CHAT_ID = '6411315434'

# Sample music paths (place your .mp3 files in 'music' folder)
MUSIC_GENRES = {
    "Lo-fi": ["music/lofi1.mp3", "music/lofi2.mp3"],
    "Chill": ["music/chill1.mp3", "music/chill2.mp3"],
    "Trap": ["music/trap1.mp3", "music/trap2.mp3"]
}

QUOTES = [
    "Believe in yourself!",
    "You are stronger than you think.",
    "Dream big and dare to fail."
]

JOKES = [
    "Why don’t scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? It had too many problems."
]

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    user = update.effective_user
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Welcome, {user.first_name}! Choose your vibe:")
    keyboard = [[InlineKeyboardButton(genre, callback_data=genre)] for genre in MUSIC_GENRES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Pick a music genre:", reply_markup=reply_markup)

    # Notify admin
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"New user started: @{user.username} ({user.id})")

def play_music(update: Update, context):
    query = update.callback_query
    genre = query.data
    song_path = random.choice(MUSIC_GENRES[genre])
    context.bot.send_audio(chat_id=query.message.chat.id, audio=open(song_path, 'rb'), caption=f"Here's some {genre} vibes!")
    query.answer()

def quote(update, context):
    update.message.reply_text(random.choice(QUOTES))

def joke(update, context):
    update.message.reply_text(random.choice(JOKES))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("quote", quote))
    dp.add_handler(CommandHandler("joke", joke))
    dp.add_handler(CallbackQueryHandler(play_music))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, ConversationHandler
import sqlite3

ADMIN_ID = []

def admin_menu(update, context):
    user_id = update.message.from_user.id
    print(user_id)
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE user_id = ?", (user_id,))
    user_idd = c.fetchone()
    keyboard = [
        [
            KeyboardButton(text='✍️Xabar yuborish✍️'),
            KeyboardButton(text='👤Foydalnuvchi malumoti📝'),
        ],
        [
            KeyboardButton(text='➕Admin qo\'shish➕'),
            KeyboardButton(text='➖Admin o\'chirish➖'),
        ],
        [
        KeyboardButton(text="📊Bot Statistika📊")
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    if user_idd:
        update.message.reply_text("Salom! Siz admin paneldasiz!", reply_markup=reply_markup)
    else:
        pass
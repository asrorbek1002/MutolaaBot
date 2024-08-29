import logging
import sqlite3
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, InlineQueryHandler
from botfunction.wikipedia_func import wiki_hand
from botfunction.register_bot import register_handler
from botfunction.add_book_base import admin_not_confirmed_book, add_book_base_handler
from botfunction.view_book import view_book_hand, view_book_for_send
from botfunction.global_text import START_TEXT, HELP
from botfunction.admin_menu import admin_menu
from botfunction.add_admin import add_admin_hand
from botfunction.send_message import send_message_hand, send_video_message_hand, send_menu
from botfunction.del_admin import del_admin_hand
from botfunction.users_date import menu_date, all_user, inlie_menu_date, nameuserdatehand, user_id_datehand

# Logging konfiguratsiyasi
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

conn = sqlite3.connect("MutolaaBot.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users
            (user_id INTEGER PRIMARY KEY,
            phone_number TEXT, 
            first_name TEXT, 
            last_name TEXT, 
            age INTEGER, 
            gender TEXT, 
            address TEXT, 
            latitude REAL,
            longitude REAL
            );
""")
c.execute("""CREATE TABLE IF NOT EXISTS books
          (user_id INTEGER,
          first_name TEXT,
          book_id TEXT PRIMARY KEY,
          book_title TEXT UNIQUE,
          book_author TEXT,
          book_lang TEXT,
          book_about TEXT,
          status TEXT)""")
c.execute('''
        CREATE TABLE IF NOT EXISTS notregisterusers (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            user_id INTEGER UNIQUE);''')
conn.commit()


# Foydalanuvchiga ko'rinadigan tugmalar
keyboard_button = [
    [
        KeyboardButton(text="📖Kitob o'qish📖"),
        KeyboardButton(text="📚Kitob qo'shish📚")
    ],
    [
        KeyboardButton(text="🌐Wikipedia🌐"),
        KeyboardButton(text="⁉️Yordam⁉️")
    ]
]
reply_markup = ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True)

def add_user_to_db(user_id, first_name, last_name):
    conn = sqlite3.connect('MutolaaBot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO notregisterusers (user_id, first_name, last_name)
        VALUES (?, ?, ?);
    ''', (user_id, first_name, last_name))
    conn.commit()
    conn.close()

def start(update, context):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    add_user_to_db(user_id, first_name, last_name)
    update.message.reply_text(
        f"Assalomu alaykum, <a href='tg://user?id={user_id}'>{first_name}</a>!\n\n{START_TEXT}", parse_mode="HTML",
        reply_markup=reply_markup)


# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Jarayon bekor qilindi!', reply_markup=reply_markup)
    return ConversationHandler.END


def get_user_count():
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    count = c.fetchone()[0]
    conn.close()
    return count

def get_notr_user_count():
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM notregisterusers')
    count = c.fetchone()[0]
    conn.close()
    return count

def get_book_count():
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM books')
    count = c.fetchone()[0]
    conn.close()
    return count

def stats(update, context):
    user_count = get_notr_user_count()
    user_register = get_user_count()
    book_count = get_book_count()
    update.message.reply_text(f"📊Bot statistikasi❕\n\nBotdagi barcha foydalanuvchilari soni: {user_count} \nBotdagi barcha kitoblar soni: {book_count}\nRo'yxatdan o'tganlar: {user_register}")

def help(update, context):
    update.message.reply_text(text=HELP, parse_mode="HTML")



def main():
    """Start the bot."""
    # Telegram Bot tokenini yuklab olish
    updater = Updater("6991187240:AAEBeLuIVyYUaIxgK__n9-r9J3FSFBTVIms")

    # Buyruqlarni qayta ishlash uchun dispetcherni yaratish
    dp = updater.dispatcher

    dp.add_handler(register_handler())
    dp.add_handler(add_book_base_handler())
    dp.add_handler(wiki_hand())
    dp.add_handler(view_book_hand())
    dp.add_handler(add_admin_hand())
    dp.add_handler(del_admin_hand())
    dp.add_handler(nameuserdatehand())
    dp.add_handler(user_id_datehand())
    dp.add_handler(send_message_hand())
    
    dp.add_handler(send_video_message_hand())
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.regex(r"^⁉️Yordam⁉️$"), help))
    dp.add_handler(CommandHandler("start", admin_not_confirmed_book, Filters.regex("Confirmed")))
    dp.add_handler(MessageHandler(Filters.regex(r"^📊Bot Statistika📊$"), stats))
    dp.add_handler(MessageHandler(Filters.regex(r"^👤Foydalnuvchi malumoti📝$"), menu_date))
    dp.add_handler(MessageHandler(Filters.regex(r"^Barcha foydalanuvchilar$"), all_user))
    dp.add_handler(MessageHandler(Filters.regex(r"^Bitta foydalanuvchi$"), inlie_menu_date))
    dp.add_handler(MessageHandler(Filters.regex(r"^✍️Xabar yuborish✍️$"), send_menu))
    dp.add_handler(CommandHandler('book_title', view_book_for_send))
    dp.add_handler(CommandHandler('admin', admin_menu))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

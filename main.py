import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler, InlineQueryHandler
from botfunction.wikipedia_func import search, start_search
from botfunction.register_bot import first_name, last_name, age, gender, geolocation, phone_number
from botfunction.add_book_base import admin_not_confirmed_book, add_book_base_handler
from botfunction.view_book import view_book_hand, view_book_for_send
import sqlite3
from functools import wraps
from botfunction.global_text import START_TEXT, HELP
from botfunction.admin_menu import admin_menu
from botfunction.add_admin import start_add_admin, addd_admin
from botfunction.del_admin import del_adminstart, del_admindel
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
    ],
    [
        KeyboardButton(text="📊Bot Statistika📊")
    ]
]
reply_markup = ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True)


# /start buyrug'iga javob qaytarish

def start(update, context):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name

    conn = sqlite3.connect("MutolaaBot.db")
    c = conn.cursor()
    c.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
    user = c.fetchone()

    # Agar foydalanuvchi topilmasa, o'zingizni tanituvchi xabarni yuboring
    reply_markup_contact = ReplyKeyboardMarkup([
        [KeyboardButton(text="Telefon kontaktinngizni ulashing", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    if user is None:
        update.message.reply_text(
            f"Assalomu alaykum <a href='tg://user?id={user_id}'>{first_name}</a>! Uzur sizni tanimadim iltimos raqamingizni menga yuboring.",
            parse_mode="HTML", reply_markup=reply_markup_contact)
        return 'PHONE_NUMBER'
    else:
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

def get_book_count():
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM books')
    count = c.fetchone()[0]
    conn.close()
    return count

def stats(update, context):
    user_count = get_user_count()
    book_count = get_book_count()
    update.message.reply_text(f"📊Bot statistikasi❕\n\nBot foydalanuvchilari soni: {user_count} \n\nBotdagi barcha kitoblar soni: {book_count}")

def help(update, context):
    update.message.reply_text(text=HELP, parse_mode="HTML")



def main():
    """Start the bot."""
    # Telegram Bot tokenini yuklab olish
    updater = Updater("6991187240:AAFOgEgjJasiOkmSmA5X2pFB9Ju9lgWD_Q4")

    # Buyruqlarni qayta ishlash uchun dispetcherni yaratish
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^⁉️Yordam⁉️$"), help))
    dispatcher.add_handler(CommandHandler("start", admin_not_confirmed_book, Filters.regex("Confirmed")))

    register_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            'PHONE_NUMBER': [MessageHandler(Filters.contact & ~Filters.command, phone_number)],
            'FIRST_NAME': [MessageHandler(Filters.text & ~Filters.command, first_name)],
            'LAST_NAME': [MessageHandler(Filters.text & ~Filters.command, last_name)],
            'AGE': [MessageHandler(Filters.text & ~Filters.command, age)],
            'GENDER': [MessageHandler(Filters.text & ~Filters.command, gender)],
            'GEOLOCATION': [MessageHandler(Filters.location & ~Filters.command, geolocation)],

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(register_handler)


    dispatcher.add_handler(add_book_base_handler())

    dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^🌐Wikipedia🌐"), start_search)],
        states={
            'SEARCH_WIKI': [MessageHandler(Filters.text, search)],
        },
        fallbacks=[MessageHandler(Filters.regex("^🔙Ortga qaytish🔙$"), cancel)]
    ))

    dispatcher.add_handler(view_book_hand())

    dispatcher.add_handler(CommandHandler('admin', admin_menu))
    add_admin = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^➕Admin qo'shish➕$"), start_add_admin)],
        states={
            'ADD_ADMIN': [MessageHandler(Filters.text & ~Filters.command, addd_admin)]            
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(add_admin)

    del_admin = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^➖Admin o'chirish➖$"), del_adminstart)],
        states={
            'DELL_ADMIN': [MessageHandler(Filters.text & ~Filters.command, del_admindel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(del_admin)
    dispatcher.add_handler(nameuserdatehand())
    dispatcher.add_handler(user_id_datehand())
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^📊Bot Statistika📊$"), stats))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^👤Foydalnuvchi malumoti📝$"), menu_date))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Barcha foydalanuvchilar$"), all_user))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^Bitta foydalanuvchi$"), inlie_menu_date))
    dispatcher.add_handler(CommandHandler('book_title', view_book_for_send))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

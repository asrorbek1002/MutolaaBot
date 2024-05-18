import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from botfunction.wikipedia_func import search, start_search
from botfunction.register_bot import first_name, last_name, age, gender, geolocation, phone_number
from botfunction.add_book_base import start_addBook, book_about, book_author, book_file, book_lang, book_title, \
    admin_not_confirmed_book
from botfunction.view_book import view_book_for_send, view_book_for_send2, view_menu, text_menu
import sqlite3
from functools import wraps
from botfunction.global_text import START_TEXT, HELP

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


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


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
    updater = Updater("6363399370:AAHLMGGBku07YSYKGcL5rMq2e5BFS1izc3A")

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

    add_book_hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^📚Kitob qo'shish📚$"), start_addBook)],
        fallbacks=[CommandHandler('cancel', cancel)],
        states={
            'BOOK_TITLE': [MessageHandler(Filters.text & ~Filters.command, book_title)],
            'BOOK_AUTHOR': [MessageHandler(Filters.text & ~Filters.command, book_author)],
            'BOOK_LANG': [MessageHandler(Filters.text & ~Filters.command, book_lang)],
            'BOOK_ABOUT': [MessageHandler(Filters.text & ~Filters.command, book_about)],
            'BOOK_FILE': [MessageHandler(Filters.document & ~Filters.command, book_file)]
        }

    )
    dispatcher.add_handler(add_book_hand)

    dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^🌐Wikipedia🌐"), start_search)],
        states={
            'SEARCH_WIKI': [MessageHandler(Filters.text, search)],
        },
        fallbacks=[MessageHandler(Filters.regex("^🔙Ortga qaytish🔙$"), cancel)]
    ))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^📖Kitob o'qish📖$"), view_menu)],
        states={
            'START_VIEW': [MessageHandler(Filters.text, text_menu)],
            'START_BOOK_TITLE_VIEW': [MessageHandler(Filters.text, view_book_for_send)],
            'START_BOOK_AUTHOR_VIEW': [MessageHandler(Filters.text, view_book_for_send2)]
        },
        fallbacks=[MessageHandler(Filters.regex(r"^🔙Ortga🔙$"), cancel)]
    ))
    dispatcher.add_handler(MessageHandler(Filters.regex(r"^📊Bot Statistika📊$"), stats))
    dispatcher.add_handler(CommandHandler('book_title', view_book_for_send))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

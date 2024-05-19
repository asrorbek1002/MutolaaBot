import sqlite3
from telegram import InlineKeyboardButton,  InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler


A_STATUS = "Tasdiqlanmagan"
B_STATUS = "Tasdiqlangan"

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

def book_title_view(book_title):
    book = book_title
    conn = sqlite3.connect("MutolaaBot.db")
    cursor = conn.cursor()

    # Kitob nomi bo'yicha ma'lumot qidirish
    cursor.execute("SELECT * FROM books WHERE book_title LIKE ?", ('%' + book + '%',))
    result = cursor.fetchall()
    print(result)
    return(result)

def book_author_view(book_author):
    book = book_author
    conn = sqlite3.connect("MutolaaBot.db")
    cursor = conn.cursor()

    # Kitob nomi bo'yicha ma'lumot qidirish
    cursor.execute("SELECT * FROM books WHERE book_author LIKE ?", ('%' + book + '%',))
    result = cursor.fetchall()
    print(result)
    return(result)

            
def view_menu(update, context):
    first_name = update.message.from_user.first_name
    kkeyboard_button = [
        [KeyboardButton(text="Kitob Nomi"), KeyboardButton(text="Kitob muallifi")],
        [KeyboardButton(text="🔙Ortga🔙")]
    ]
    reply_markup = ReplyKeyboardMarkup(kkeyboard_button, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(f"Xo'sh {first_name}, Botdan kitobni qaysi usul bilan qidirishni tanlang", reply_markup=reply_markup)
    return 'START_VIEW'

def text_menu(update, context):
    message = update.message.text
    
    if message =='Kitob Nomi':
        update.message.reply_text("Yaxshi! Kitobni topish uchun uning nomini xatolarsiz kiriting ilitmos.")
        return 'START_BOOK_TITLE_VIEW'
    elif message == 'Kitob muallifi':
        update.message.reply_text("Yaxshi! Kitobni muallifini ismini xatolarsiz kiriting ilitmos.\nShunda aniq natijalar chiqdi")
        return 'START_BOOK_AUTHOR_VIEW'
    elif message == '🔙Ortga🔙':
        update.message.reply_text("Asosiy menu.", reply_markup=reply_markup)
        return ConversationHandler.END#and start(update, context)
    else:
        update.message.reply_text("Jarayon bekor qilindi.\nSiz faqat pastdagi tugmalarni ishlatishingiz kerak.", reply_markup=reply_markup)
        return ConversationHandler.END



def view_book_for_send(update, context):
    user_id = update.message.from_user.id
    book_title = update.message.text
    book = book_title_view(book_title)
    if book:    
        for bok in book:
            if bok[7] == B_STATUS:
                book_id = bok[2]
                book_name = bok[3]
                book_author = bok[4]
                book_lang = bok[5]
                book_about = bok[6]
                context.bot.send_document(chat_id=user_id, document=book_id, caption=f"""
👤Muallif: {book_author}
📙Kitob nomi: {book_name}
🏴Kitob tili: {book_lang}

❕Bu kitob: {book_about}""")
            else:
                update.message.reply_text("Uzur botda bunday kitob yo'q ekan tez orada kitob botga qo'shiladi.", reply_markup=reply_markup)
                return ConversationHandler.END
    else:
        update.message.reply_text("Uzur botda bunday kitob yo'q ekan tez orada kitob botga qo'shiladi.", reply_markup=reply_markup)
        return ConversationHandler.END
    
    
def view_book_for_send2(update, context):
    user_id = update.message.from_user.id
    book_author = update.message.text
    book = book_author_view(book_author)
    if book:    
        for bok in book:
            if bok[7] == B_STATUS:
                book_id = bok[2]
                book_name = bok[3]
                book_author = bok[4]
                book_lang = bok[5]
                book_about = bok[6]
                context.bot.send_document(chat_id=user_id, document=book_id, caption=f"""
👤Muallif: {book_author}
📙Kitob nomi: {book_name}
🏴Kitob tili: {book_lang}

❕Bu kitob: {book_about}""")
            else:
                update.message.reply_text("<b>Kitob topilmadi🫤</b>.\nBotimizni tark etmang tez orada ko'plab kitoblar qo'shiladi.", parse_mode="HTML", reply_markup=reply_markup)
                return ConversationHandler.END
    else:
        update.message.reply_text("<b>Kitob topilmadi🫤</b>.\nBotimizni tark etmang tez orada ko'plab kitoblar qo'shiladi.", parse_mode="HTML", reply_markup=reply_markup)
        return ConversationHandler.END
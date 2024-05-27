import sqlite3
import os
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import xlsxwriter


keyboard = [
        [
            KeyboardButton(text='✍️Xabar yuborish✍️'),
            KeyboardButton(text='👤Foydalnuvchi malumoti📝'),
        ],
        [
            KeyboardButton(text='➕Admin qo\'shish➕'),
            KeyboardButton(text='➖Admin o\'chirish➖'),
        ]
    ]
reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)




def menu_date(update, context):
    keyboard = [
        [KeyboardButton(text="Barcha foydalanuvchilar"), KeyboardButton(text="Bitta foydalanuvchi")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text("Kerakli tugmani tanlang", reply_markup=reply_markup)

def inlie_menu_date(update, context):
    inline_keyboard = [
        [KeyboardButton(text="Ismi orqali"),
         KeyboardButton(text="Telegram ID orqali")]
    ]
    reply_markup = ReplyKeyboardMarkup(inline_keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Foyydalanuvchi maumotini qaysi yo'l bilan qidirmoqchisiz", reply_markup=reply_markup)


def sql_to_xlsx():
    workbook = xlsxwriter.Workbook('date.xlsx') # Create file
    conn = sqlite3.connect('MutolaaBot.db') # Connect to your database
    cursor = conn.cursor() # Create the cursor
    tables = list(cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")) # Get all table names
    tables = list(map(lambda x: x[0], tables)) # convert the list of tuple to list of str
    for table in tables:
        try: worksheet = workbook.add_worksheet(name=table[0:31]) # Sheet names in excel can have up to 31 chars
        except:pass
        for row_number, row in enumerate(cursor.execute('SELECT * FROM '+table)): # row is a tuple here
            for column_number, item in enumerate(row):
                try: worksheet.write(row_number, column_number, item) # Write the cell in the current sheet
                except:pass
    workbook.close() 


def all_user(update, context):
    user_id = update.message.from_user.id
    create_date = sql_to_xlsx()
    with open('date.xlsx', 'rb') as file:
        context.bot.send_document(chat_id=user_id, document=file, filename="Botning bazasi.xlsx", caption="Botdagi barcha foydalanuvchilarning va kitoblarning malumotlari")
    
    os.remove('date.xlsx')


def one_userFirstname(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(chat_id=user_id, text="Iltimos kimni malumoti kerak bo'lsa uning ismini kiriting")
    return 'DATE_USER_OF_NAME'


def one_user_firstname(update, context):
    first_name = update.message.text
    user_id = update.message.from_user.id
    conn = sqlite3.connect("MutolaaBot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE first_name LIKE ?",  ('%' + first_name + '%',))
    user_date = c.fetchall()
    if user_date:
        for i in user_date:
            context.bot.send_message(chat_id=user_id, text=f"Foydalanuvchi Id: {i[0]}\nTelefon raqam: {i[1]}\nIsm: {i[2]}\nFamiliya: {i[3]}\nYosh: {i[4]}\nJinsi: {i[5]}\nManzili: {i[6]}")
            context.bot.send_location(chat_id=user_id, latitude=i[7], longitude=i[8])
        print(f'Malumot Bor {user_date}')
    else:
        update.message.reply_text("Malumot topilmadi\n/admin")
        return ConversationHandler.END
    

# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Jarayon bekor qilindi!', reply_markup=reply_markup)
    return ConversationHandler.END


def one_useruser_id(update, context):
    user_id = update.message.from_user.id
    context.bot.send_message(chat_id=user_id, text="Iltimos kimni malumoti kerak bo'lsa uning telegram idsini kiriting")
    return 'DATE_USER_OF_NAME'


def one_user_user_id(update, context):
    user_id_date = str(update.message.text)
    user_id = update.message.from_user.id
    conn = sqlite3.connect("MutolaaBot.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id LIKE ?",  ('%' + user_id_date + '%',))
    user_date = c.fetchall()
    if user_date:
        for i in user_date:
            context.bot.send_message(chat_id=user_id, text=f"Foydalanuvchi Id: {i[0]}\nTelefon raqam: {i[1]}\nIsm: {i[2]}\nFamiliya: {i[3]}\nYosh: {i[4]}\nJinsi: {i[5]}\nManzili: {i[6]}")
            context.bot.send_location(chat_id=user_id, latitude=i[7], longitude=i[8])
        # print(f'Malumot Bor {user_date}')
    else:
        update.message.reply_text("Malumot topilmadi\n/admin")
        return ConversationHandler.END

def user_id_datehand():
    handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^Telegram ID orqali$"), one_useruser_id)],
        states={
            'DATE_USER_OF_NAME': [MessageHandler(Filters.text, one_user_user_id)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler

def nameuserdatehand():
    handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^Ismi orqali$"), one_userFirstname)],
        states={
            'DATE_USER_OF_NAME': [MessageHandler(Filters.text, one_user_firstname)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return handler
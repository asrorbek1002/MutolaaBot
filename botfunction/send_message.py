import sqlite3

from telegram import TelegramError, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

conn = sqlite3.connect('MutolaaBot.db')
cursor = conn.cursor()
# Ma'lumotlarni olish
cursor.execute("SELECT user_id FROM admins")
results = cursor.fetchall()
print(results[0])
print(results)
ADMIN_ID = results

def send_menu(update, context):
    keyboard = [
        [KeyboardButton(text="Oddiy xabar"), KeyboardButton(text="📹Video Xabar📹")],
        [KeyboardButton(text="🖼Foto xabar🖼"), KeyboardButton(text="📁Fayl xabar📂")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text('Qaysi turdagi xabarni yubormoqchisiz?', reply_markup=reply_markup)



def xabarlar(update, context):
    text = update.message.text
    if text == "Oddiy xabar":
        return 'TEXT_MESSAGE'
    elif text == "Video xabar":
        update.message.reply_text('Yubormoqchi bo\'lgan videoni yuboring')
        return 'VIDEO_MESSAGE'
    elif text == "Foto xabar":
        update.message.reply_text('Yubormoqchi bo\'lgan rasmni yuboring')
        return 'FOTO_MESSAGE'
    elif text == "Fayl xabar":
        update.message.reply_text('Yubormoqchi bo\'lgan faylni yuboring')
        return 'FAYL_MESSAGE'
    
def send_mm(update, context):
    user_id = update.message.from_user.id
    if user_id in ADMIN_ID:
        update.message.reply_text("Foydalanuvchilarga yubormoqchi bo'lga xabarni kiriting...")
    else:pass
    return 'SEND_MESSAGE1'

def send_m(update, context):
    # SQLite bazasiga ulanish
    conn = sqlite3.connect('MutolaaBot.db')
    cursor = conn.cursor()
    # Ma'lumotlarni olish
    cursor.execute("SELECT user_id FROM users")
    results = cursor.fetchall()

    message = update.message.text

    count = 0
    for result in results:
        user_id = result[0]
        try:
            context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except TelegramError as e:
            print(e)


    cursor.close()
    conn.close()
    context.bot.send_message(chat_id=ADMIN_ID, text=f'Xabar {count}-kishiga yborildi')
    return ConversationHandler.END
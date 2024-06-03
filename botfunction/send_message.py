import sqlite3

from telegram import TelegramError, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, Filters, CommandHandler

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



# def xabarlar(update, context):
#     text = update.message.text
#     if text == "Oddiy xabar":
#         return 'TEXT_MESSAGE'
#     elif text == "Video xabar":
#         update.message.reply_text('Yubormoqchi bo\'lgan videoni yuboring')
#         return 'VIDEO_MESSAGE'
#     elif text == "Foto xabar":
#         update.message.reply_text('Yubormoqchi bo\'lgan rasmni yuboring')
#         return 'FOTO_MESSAGE'
#     elif text == "Fayl xabar":
#         update.message.reply_text('Yubormoqchi bo\'lgan faylni yuboring')
#         return 'FAYL_MESSAGE'
    
def send_mm(update, context):
    user_id = update.message.from_user.id
    if user_id in ADMIN_ID:
        update.message.reply_text("Foydalanuvchilarga yubormoqchi bo'lga xabarni kiriting...")
    else:pass
    return 'SEND_MESSAGE'

def send_m(update, context):
    # SQLite bazasiga ulanish
    conn = sqlite3.connect('MutolaaBot.db')
    cursor = conn.cursor()
    # Ma'lumotlarni olish
    cursor.execute("SELECT user_id FROM notregisterusers")
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

def sed_video_message(update, context):
    update.message.reply_text("Foydalanuvchilarga yubormoqchi bo'gan videoni yuboring")
    return  'SEND_VIDEO'

def sendvideo(update, context):
    video_id = update.message.video.file_id
    print(video_id)
    context.user_data['video_id'] = video_id
    update.message.reply_text("Endi video tavsifini yozing")
    return 'SEND_VIDEO_MSG'

def allusersendvideo(update, context):
    conn = sqlite3.connect('MutolaaBot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM notregisterusers")
    results = cursor.fetchall()
    message = update.message.text
    count = 0
    for result in results:
        user_id = result[0]
        try:
            update.message.reply_video(video=context.user_data['video_id'], caption=message)
            count += 1
        except TelegramError as e:
            print(e)
    cursor.close()
    conn.close()
    context.bot.send_message(chat_id=ADMIN_ID, text=f'Xabar {count}-kishiga yborildi')
    return ConversationHandler.END

# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Jarayon bekor qilindi!')
    return ConversationHandler.END

def send_video_message_hand():
    hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^📹Video Xabar📹$"), sed_video_message)],
        states={
            'SEND_VIDEO':[MessageHandler(Filters.video, sendvideo)],
            'SEND_VIDEO_MSG':[MessageHandler(Filters.text & ~Filters.command, allusersendvideo)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return hand

def send_message_hand():
    hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^Oddiy xabar$"), send_mm)],
        states={
            'SEND_MESSAGE': [MessageHandler(Filters.text, send_m)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return hand
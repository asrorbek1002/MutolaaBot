import sqlite3
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler

conn = sqlite3.connect('./MutolaaBot.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS admins
(user_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
firstname TEXT);""")
count = c.execute("SELECT COUNT(*) FROM admins")
if count.fetchone()[0] == 0:
    c.execute("INSERT INTO admins VALUES (?,?)", (6194484795, 'Asrorbek'))
    conn.commit()
else:
    conn.commit()


def start_add_admin(update, context):
    update.message.reply_text("Iltimos foydalnuvhining telegram idsini kiriting\n\nJarayonni bekor qilish /cancel")
    return 'ADD_ADMIN'


def addd_admin(update, context):
    text = update.message.text
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id = ?", (text,))
    users_result = c.fetchone()
    print(users_result)
    if users_result:
        c.execute("SELECT user_id FROM admins WHERE user_id = ?", (text,))
        admin_result = c.fetchone()
        print(admin_result)
        if admin_result is None:
            user_id = users_result[0]
            firstname = users_result[2]
            c.execute("INSERT INTO admins VALUES (?,?)", (user_id, firstname))
            conn.commit()
            update.message.reply_text(f"<a href='tg://user?id={user_id}'>{firstname}</a> adminlar ro'yxatiga qo'shildi")
            context.bot.send_message(chat_id=user_id, text=f"{firstname} Sizni tabriklaymiz siz hozrigina admin bo'ldingiz")
        elif admin_result:
            update.message.reply_text("Bu foydalanuvchi avvaldan admin bo'lgan")
    else:
        update.message.reply_text("Bunday foydalanuvchi botda yo'q")
    return ConversationHandler.END


# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Jarayon bekor qilindi!')
    return ConversationHandler.END



def add_admin_hand():
    add_admin = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^➕Admin qo'shish➕$"), start_add_admin)],
        states={
            'ADD_ADMIN': [MessageHandler(Filters.text & ~Filters.command, addd_admin)]            
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return add_admin
import sqlite3
import json

from telegram.ext import ConversationHandler

conn = sqlite3.connect('../MutolaaBot.db')
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
    connect = sqlite3.connect('../MutolaaBot.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (text,))
    users_result = cursor.fetchone()
    if users_result:
        cursor.execute("SELECT user_id FROM admins WHERE user_id = ?", (text,))
        admin_result = cursor.fetchone()
        if admin_result is None:
            user_id = users_result[0]
            firstname = users_result[2]
            cursor.execute("INSERT INTO admins VALUES (?,?)", (user_id, firstname))
            connect.commit()
            update.message.reply_text(f"<a href='tg://user?id={user_id}'>{firstname}</a> adminlar ro'yxatiga qo'shildi")
            context.bot.send_message(chat_id=user_id, text=f"{firstname} Sizni tabriklaymiz siz hozrigina admin bo'ldingiz")
        elif admin_result:
            update.message.reply_text("Bu foydalanuvchi avvaldan admin bo'lgan")
    else:
        update.message.reply_text("Bunday foydalanuvchi botda yo'q")
    return ConversationHandler.END
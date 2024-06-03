import sqlite3
from telegram.ext import ConversationHandler, MessageHandler, Filters,  CommandHandler
from telegram.error import TelegramError


def del_admin(user_id):
    user_id = user_id
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM admins WHERE user_id=?", (user_id,))
    people = c.fetchone()
    print(people)
    if people:
        c.execute('DELETE FROM admins WHERE user_id=?', (user_id,))
        conn.commit()
        conn.close()
        return True
    elif people is None:
        return False



def del_adminstart(update, context):
    update.message.reply_text("Adminlikdan o'chirmoqchi bo'lgan foydalnuvchi ID sini yuboring...")
    return 'DELL_ADMIN'

def del_admindel(update, context):
    del_user_id = update.message.text
    print(type(del_user_id))
    user_id = update.message.from_user.id
    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    # c.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id))
    yes_admin = 'True'
    print(yes_admin)
    if yes_admin:
        delete = del_admin(user_id=del_user_id)
        if delete is True:
            update.message.reply_text("Foydalanuvchi adminlikdan bo'shatildi")
            context.bot.send_message(chat_id=del_user_id, text="Afsuski sizni adminlik lavozimidan ozod qilishdi")
        elif delete is False:
            update.message.reply_text("Qandaydir xaatolik tufayli foydalnuvchi adminlikda bo'shatilmadi.")
    elif yes_admin is None:
        update.message.reply_text("Siz admin emassiz")
    return ConversationHandler.END


# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Jarayon bekor qilindi!')
    return ConversationHandler.END



def del_admin_hand():
    del_admin = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^➖Admin o'chirish➖$"), del_adminstart)],
        states={
            'DELL_ADMIN': [MessageHandler(Filters.text & ~Filters.command, del_admindel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return del_admin
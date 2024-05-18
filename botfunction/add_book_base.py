import sqlite3
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

ADMIN_ID = 6194484795
A_STATUS = "Tasdiqlanmagan"
B_STATUS = "Tasdiqlangan"

def start_addBook(update, context):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    context.user_data['first_name'] = first_name
    context.user_data['user_id'] = user_id
    # rreply_markup = ReplyKeyboardMarkup([[KeyboardButton(text='❌Bekor qilish❌')]], resize_keyboard=True)
    update.message.reply_text("Botga o'z hissangizni qo'shmoqchiligingizdan biz bag'oyatda hursandmiz.\n\n<i>Sizdan iltimos siz qo'shmoqchi bo'lgan kitob botda bormi yoki yo'qligini tekshirib ko'ring</i>\n\n<b>Unday bo'lsa boshladik!!! Kitobning nomini yozing...</b>\n\nJarayonni bekor qilish uchun /cancel ni bosing", parse_mode="HTML")
    return 'BOOK_TITLE'

def book_title(update, context):
    book_title = update.message.text
    context.user_data['book_title'] = book_title
    update.message.reply_text(f"Yaxshi!\n\n<b>📓 Kitob nomi: {book_title} </b>\nUning muallifi kim?", parse_mode="HTML")
    return 'BOOK_AUTHOR'

def book_author(update, context):
    book_author = update.message.text
    context.user_data['book_author'] = book_author
    update.message.reply_text(f"Judda ajoyib😉\n<b>📓 Kitob nomi: {context.user_data['book_title']}\n👤Muallif: {book_author}</b>\n\nEndi kitob qaysi tildaligi va agar tarjimasi bo'lsa tarjima tili\n<i>Misol: Ingliz(Uzbek)</i>", parse_mode="HTML")
    return 'BOOK_LANG'

def book_lang(update, context):
    book_lang = update.message.text
    context.user_data['book_lang'] = book_lang
    update.message.reply_text(f"Ajoyib😍.\n<b>📓 Kitob nomi: {context.user_data['book_title']}\n👤Muallif: {context.user_data['book_author']}\n🌐Kitob tili: {book_lang}</b>\n\nEndi kitob haqida qisqacha tavsif yozing foydalanuvchi bu kitob nima haqida ekanligini onson bilish uchun", parse_mode="HTML")
    return 'BOOK_ABOUT'

def book_about(update, context):
    book_about = update.message.text
    context.user_data['book_about'] = book_about
    update.message.reply_text(f"Qoyilmaqom🤩\n<b>📓 Kitob nomi: {context.user_data['book_title']}\n👤Muallif: {context.user_data['book_author']}\n🌐Kitob tili: {context.user_data['book_lang']}\n\n📖Kitob haqida: <i>{context.user_data['book_about']}</i></b>\n\n<b>Endi kitobning PDF shaklini menga yuboring</b>.", parse_mode="HTML")
    return 'BOOK_FILE'



def book_file(update, context):
    first_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    book_id = update.message.document.file_id
    bot_username = context.bot.username
    print(book_id)
    print(bot_username)
    context.user_data['book_id'] = book_id
    context.user_data['status'] = A_STATUS
    conn = sqlite3.connect("MutolaaBot.db")
    c = conn.cursor()
    string = context.user_data['book_title']
    kitob_nomi = string.replace(" ", "_")
    try:
        c.execute("INSERT INTO books VALUES (?,?,?,?,?,?,?,?)", 
                (context.user_data['user_id'],
                context.user_data['first_name'],
                context.user_data['book_id'],
                context.user_data['book_title'],
                context.user_data['book_author'],
                context.user_data['book_lang'],
                context.user_data['book_about'],
                context.user_data['status']
                ))
        
        conn.commit()
        update.message.reply_text("<b>Botga hissangizni qo'shganingiz uchun katta rahmat</b>.\n<b>Siz qo'shgan kitob adminga yuborildi.</b>\n<i>Admin kitobni ko'rib chiqib tez orada tasdiqaydi, undan keyin kitobingizdan hamma foydalanishi mumikin bo'ladi</i>.", parse_mode="HTML")
        context.bot.send_document(chat_id=ADMIN_ID, document=book_id,
                              caption=f"""Admin botga <a href='tg://user?id={user_id}'>{first_name}</a> yangi kitob qo'shmoqchi
            
                              
<b>Kitob nomi: {context.user_data['book_title']}
Kitob muallifi: {context.user_data['book_author']}
Kitob tili: {context.user_data['book_lang']}

Kitob tavsifi: {context.user_data['book_about']}
</b>
<i>Status: {A_STATUS}</i>""", parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="✅Tasdiqlash✅", url=f"https://t.me/{bot_username}?start=ConfirmedBook_{kitob_nomi}")
    ],
    [
        InlineKeyboardButton(text="❌ Rad etish ❌", url=f"https://t.me/{bot_username}?start=NotConfirmedBook_{kitob_nomi}")
    ]
]))
        
    except sqlite3.Error as e:
        print(f'Xatolik {e}')
        context.bot.send_message(chat_id=user_id, text="⚠️Nomalum xatolik ro'y berdi.\nMa'lumotlaringiz Adminga yuborildi tez orada ko'rib chiqadi.")
    
        context.bot.send_document(chat_id=ADMIN_ID, document=book_id,
                              caption=f"""Admin botga <a href='tg://user?id={user_id}'>{first_name}</a> yangi kitob qo'shmoqchi edi xatolik bo'ldi.
                              

Kitob nomi: {context.user_data['book_title']}
Kitob muallifi: {context.user_data['book_author']}
Kitob tili: {context.user_data['book_lang']}

Kitob tavsifi: {context.user_data['book_about']}

Status: {A_STATUS}""", parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
    [
        InlineKeyboardButton(text="✅Tasdiqlash✅", url=f"https://t.me/{bot_username}?start=ConfirmedBook_{kitob_nomi}")
    ],
    [
        InlineKeyboardButton(text="❌ Rad etish ❌", url=f"https://t.me/{bot_username}?start=NotConfirmedBook_{kitob_nomi}")
    ]
]))


# def admin_confirm_book(update, context):
#     text = context.args[0]
#     textlist = text.split("_")
#     noldelete = textlist.pop(0)  
#     book_name = " ".join(textlist)
#     conn = sqlite3.connect("MutolaaBot.db")
    # cursor = conn.cursor()
    # # Kitob nomi bo'yicha ma'lumot qidirish
    # cursor.execute("SELECT * FROM books WHERE book_title LIKE ?", ('%' + book_name + '%',))
    # result = cursor.fetchone()
    # user_id = result[0]
    # first_name = result[1]

    # # Agar malumot topilsa
    # if result:
    #     # Statusni "Tasdiqlangan" deb o'zgartirish
    #     cursor.execute("UPDATE books SET status = ? WHERE book_title = ?", (B_STATUS, book_name))
    #     conn.commit()
    #     context.bot.send_message(chat_id=user_id, text=f'{first_name} tabriklayman kitobingiz tasdiqdan o\'tdi!\n\nSiz joylagan kitobdan endi hamma foydalanishi mumkin.')
    #     print(f"Kitob nomi \"{book_name}\" uchun status \"Tasdiqlangan\" ga o'zgartirildi.")
    # else:
    #     print("Uzr, malumot topilmadi.")
    # print(book_name)
    # print(text)

def admin_not_confirmed_book(update, context):
    text = context.args
    text2 = text[0]
    if text:
        textlist = text2.split("_")
        noldelete = textlist.pop(0)
        conn = sqlite3.connect('MutolaaBot.db')
        cursor = conn.cursor()
        print(f'NolDel: {noldelete}')
        if noldelete == 'NotConfirmedBook':  
            book_name = " ".join(textlist)
            cursor.execute("SELECT * FROM books WHERE book_title=?", (book_name,))
            row = cursor.fetchone()

            if row:
                # Ma'lumot topilganligi
                context.bot.send_message(chat_id=update.effective_chat.id, text="Kitob topildi")

                # Ma'lumotni o'chirish
                cursor.execute("DELETE FROM books WHERE book_id=?", (row[2],))
                conn.commit()
                context.bot.send_message(chat_id=row[0], text=f'{row[1]} ma\'lum bir sabablarga ko\'ra sizning kitobingiz tasdiqdan o\'tmadi.\n\nBatafsil tafsilotlarni admindan so\'rab olishingiz mumkin.')
                context.bot.send_message(chat_id=update.effective_chat.id, text="Ma'lumot o'chirildi.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Ma'lumot topilmadi.")
        elif noldelete == 'ConfirmedBook':
            book_name = " ".join(textlist)
                # Kitob nomi bo'yicha ma'lumot qidirish
            cursor.execute("SELECT * FROM books WHERE book_title LIKE ?", ('%' + book_name + '%',))
            result = cursor.fetchone()
            user_id = result[0]
            first_name = result[1]

            # Agar malumot topilsa
            if result:
                # Statusni "Tasdiqlangan" deb o'zgartirish
                cursor.execute("UPDATE books SET status = ? WHERE book_title = ?", (B_STATUS, book_name))
                conn.commit()
                context.bot.send_message(chat_id=user_id, text=f'{first_name} tabriklayman kitobingiz tasdiqdan o\'tdi!\n\nSiz joylagan kitobdan endi hamma foydalanishi mumkin.')
                print(f"Kitob nomi \"{book_name}\" uchun status \"Tasdiqlangan\" ga o'zgartirildi.")
            else:
                print("Uzr, malumot topilmadi.")
    else:
        pass
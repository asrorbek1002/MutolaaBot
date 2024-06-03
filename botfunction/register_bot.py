import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
import sqlite3
from .geo_name import get_location_name

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# Foydalanuvchiga ko'rinadigan tugmalar
keyboard_button = [
    [
        KeyboardButton(text="📖Kitob o'qish📖"),
        KeyboardButton(text="📚Kitob qo'shish📚")
    ],
    [
        KeyboardButton(text="🌐Wikipedia🌐"),
        KeyboardButton(text="⁉️Yordam⁉️")
    ]
]
reply_markup = ReplyKeyboardMarkup(keyboard_button, resize_keyboard=True)



def register_start(update, context):
    reply_text = 'Botga kitob qo\'shishingizdan avval o\'zingizni taniting:'
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="Telefon kontaktinngizni ulashing", request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_user.id, text=reply_text, reply_markup=reply_markup)
    return 'PHONE_NUMBER'


def phone_number(update, context):
    phone_number = update.message.contact.phone_number
    context.user_data['phone_number'] = phone_number
    update.message.reply_text('Rahmat! Ismingiz nima?')
    return 'FIRST_NAME'


def first_name(update, context):
    first_name = update.message.text
    context.user_data['first_name'] = first_name
    update.message.reply_text('Rahmat! Familyangiz nima?')
    return 'LAST_NAME'


def last_name(update, context):
    last_name = update.message.text
    context.user_data['last_name'] = last_name
    update.message.reply_text('Rahmat! yoshingiz?')
    return 'AGE'


def age(update, context):
    age = update.message.text
    context.user_data['age'] = age
    update.message.reply_text('Rahmat! Jinsingiz: erkak/ayol?')
    return 'GENDER'


def gender(update, context):
    gender = update.message.text
    context.user_data['gender'] = gender
    reply_markup = ReplyKeyboardMarkup([
        [KeyboardButton(text="lokatsiyanngizni ulashing", request_location=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_user.id, text="lokatsiyanngizni ulashing:", reply_markup=reply_markup)
    return 'GEOLOCATION'


def geolocation(update, context):
    user_id = update.message.from_user.id
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude
    address = get_location_name(latitude, longitude)
    context.user_data['user_id'] = user_id
    context.user_data['latitude'] = latitude
    context.user_data['longitude'] = longitude
    context.user_data['address'] = address

    conn = sqlite3.connect('MutolaaBot.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)", (
        context.user_data['user_id'],
        context.user_data['phone_number'],
        context.user_data['first_name'],
        context.user_data['last_name'],
        context.user_data['age'],
        context.user_data['gender'],
        context.user_data['address'],
        context.user_data['latitude'],
        context.user_data['longitude'],
    )
            )
    conn.commit()
    conn.close()
    logging.info("User Registered")
    update.message.reply_text("Rahmat! Botdan foydalanishingiz mumkin", reply_markup=reply_markup)
    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text(text='Bekor qilindi!')
    return ConversationHandler.END



def register_handler():
    register_hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^Ro'yxatdan o'tish$"), register_start)],

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
    return register_hand
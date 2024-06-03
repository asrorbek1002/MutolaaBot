import wikipedia
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ChatAction
from telegram.ext import CallbackContext, ConversationHandler, MessageHandler, Filters, CommandHandler
from functools import wraps

# Wikipedia kutubxonasiga ulanish
wikipedia.set_lang("uz") # Maqola tilini sozlash, masalan "uz" uchun o'zbek, "en" uchun ingliz tili
wikipedia.set_rate_limiting(True) # soatda faqat qancha so'roq yuborilishi mumkinligini belgilaydi.



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



def start_search(update, context):
    update.message.reply_text("Wikipediadan malumot qidirish uchun qidirmoqchi bo'lgan so'zni kiriting!")
    return 'SEARCH_WIKI'

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func    
# /search buyrug'iga javob qaytarish
@send_typing_action
def search(update: Update, context: CallbackContext):
    query = update.message.text
    try:
        result = wikipedia.summary(query)
        update.message.reply_text(result,)
    except wikipedia.exceptions.PageError:
        update.message.reply_text("Maqola topilmadi. /start")
        return ConversationHandler.END
    except wikipedia.exceptions.DisambiguationError as e:
        update.message.reply_text("Boshqa maqolalar topildi, iltimos, qidirilayotgan mavzuni aniqroq kiritish uchun qidiruv so'zini batafsilroq yozing.", reply_markup=ReplyKeyboardMarkup([
                                      [KeyboardButton(text="🔙Ortga qaytish🔙")]
                                  ], resize_keyboard=True))
    except Exception as e:
        update.message.reply_text("Ma'lumotlar olishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.", reply_markup=ReplyKeyboardMarkup([
                                      [KeyboardButton(text="🔙Ortga qaytish🔙")]
                                  ], resize_keyboard=True))


# ConversationHandlerni tugatish uchun funksiya
def cancel(update, context):
    update.message.reply_text(text='Asosiy menu', reply_markup=reply_markup)
    return ConversationHandler.END



def wiki_hand():
    hand = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(r"^🌐Wikipedia🌐"), start_search)],
        fallbacks=[MessageHandler(Filters.regex("^🔙Ortga qaytish🔙$"), cancel)],
        states={
            'SEARCH_WIKI': [MessageHandler(Filters.text, search)],
        }   
    )
    return hand
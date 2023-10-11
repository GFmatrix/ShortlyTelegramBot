import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ParseMode, KeyboardButton
from telegram.ext import (
  Updater,
  CommandHandler,
  CallbackQueryHandler,
  ConversationHandler,
  CallbackContext,
)
from utils import *
from telegram.ext import Filters
from telegram.ext import MessageHandler
# from keyboards import *
# Enable logging
logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
MENU, CREATE_URL, CUSTOM_URL = range(3)
# Callback data
# ONE, TWO, THREE, FOUR = range(4)


def start(update: Update, context: CallbackContext) -> int:
  """Send message on `/start`."""
  update.message.reply_text(get_mes('start'), reply_markup=ReplyKeyboardMarkup([[key] for key in get_key('menu_keyboard')]))
  add_user(update.message.from_user.id)
  return MENU

def create_url(update: Update, context: CallbackContext) -> int:
  update.message.reply_text(get_mes('create_url'), reply_markup=ReplyKeyboardMarkup([[get_key('cancel')]], resize_keyboard=True))
  return CREATE_URL
 
def catch_url(update: Update, context: CallbackContext) -> int:
  url = update.message.text
  if check_url(url): 
    context.user_data['url'] = url
    keyboard =  [[
            InlineKeyboardButton("✅ Ha", callback_data='Yes'),
            InlineKeyboardButton("❌ Yoq", callback_data='No'),
    ]]
    update.message.reply_text(f"URL: {url}\nKichkina URL ga shaxsiy nom berasizmi?\n(https://short.ly/<b>YouTube</b>)", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
    return CUSTOM_URL
  else:
    update.message.reply_text(get_mes('not_valid_url'))
    return CREATE_URL

def cancel(update: Update, context: CallbackContext) -> int:
  try:update.callback_query.bot.send_message(update.callback_query.message.chat_id, get_mes('cancel'), reply_markup=ReplyKeyboardMarkup([[key] for key in get_key('menu_keyboard')]))
  except:update.message.reply_text(get_mes('cancel'), reply_markup=ReplyKeyboardMarkup([[key] for key in get_key('menu_keyboard')]))
  # 
  return MENU


def my_urls(update: Update, context: CallbackContext) -> int:
  
  pass
  # update.message.reply_text(get_mes('my_urls'))
  # return MENU

def url_stat(update: Update, context: CallbackContext) -> int:
  pass
  # update.message.reply_text(get_mes('url_stat'))
  # return MENU

def custom_url_call(update: Update, context: CallbackContext) -> int:
  query = update.callback_query
  query.answer()
  if query.data == 'Yes':
    query.edit_message_text(f"URL: {query.message.text}\nKichkina URL ga shaxsiy nom berasizmi?\n(https://short.ly/<b>YouTube</b>)", parse_mode=ParseMode.HTML)
  else:
    query.edit_message_text("Surovingiz amalga oshirilmoqda...")
    res = long_to_short(context.user_data['url'])
    if res:
      query.message.delete()
      query.bot.send_message(query.message.chat_id, f"Kichik URL: {res['shorturl']}")
      add_url(query.message.from_user.id, res)
      cancel(update, context)
    else:
      query.message.delete()
      query.bot.send_message(query.message.chat_id, "Xatolik yuz berdi, iltimos qaytadan urinib kuring.")
      cancel(update, context)
    # query.edit_message_text(f"URL: {context.user_data['url']}\nSurovingiz amalga oshirildi!\n{res}")
  return CUSTOM_URL

def help_com(update: Update, context: CallbackContext) -> int:
  pass

def main() -> None:
  """Run the bot."""
  updater = Updater("6527372080:AAEcF_9xlU6FG_R2e4Imyd2cPT0QkqL0x3o")

  dispatcher = updater.dispatcher

  conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
      MENU: [
        MessageHandler(Filters.text(key), func) for key, func in zip(get_key('menu_keyboard'), [create_url, my_urls, url_stat, help_com])
        
      ] + [CommandHandler('start', start)],
      CREATE_URL: [
        MessageHandler(Filters.text & ~Filters.text(get_key('cancel')), catch_url)
      ],
      CUSTOM_URL: [
        CallbackQueryHandler(custom_url_call),
      ],
      # SECOND: [
      #   CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
      # ],
    },
    fallbacks=[MessageHandler(Filters.text(get_key('cancel')) or Filters.text, cancel)],
  )

  # Add ConversationHandler to dispatcher that will be used for handling updates
  dispatcher.add_handler(conv_handler)

  # Start the Bot
  updater.start_polling()

  # Run the bot until you press Ctrl-C or the process receives SIGINT,
  # SIGTERM or SIGABRT. This should be used most of the time, since
  # start_polling() is non-blocking and will stop the bot gracefully.
  updater.idle()


if __name__ == '__main__':
  main()
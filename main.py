from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from secret_token import TOKEN
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Hello')

def echo(update, context):
    context.bot.send_message(update.effective_chat.id, update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(update.effective_chat.id, text_caps)

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
updater.dispatcher.add_handler(CommandHandler('caps', caps))

updater.start_polling()

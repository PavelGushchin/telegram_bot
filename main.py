#!/usr/bin/env python3

import logging

from telegram import (
    Update,
)
from telegram.ext import (
    Updater,
    CallbackContext,
    Filters,
    CommandHandler,
    MessageHandler,
)

from secret_token import TOKEN

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def help(update: Update, context: CallbackContext) -> None:
    """Function for /help command"""

    # Send help message
    update.message.reply_text(
        "What can I do:\n\n  /start - say 'hello'\n\n  /movie - suggest an interesting movie\n\n  /series - suggest an interesting TV series\n\n  /help - show help message"
    )


def start(update: Update, context: CallbackContext) -> None:
    """Function for /start command"""

    # Send "Hello" sticker
    update.message.reply_sticker("CAACAgIAAxkBAAIBdWDmwUbnbcGuw7gMeJ_JF7QQq0uaAAKZDAACP1QBSs-TDHlrwSKUIAQ")

    # Show help message
    help(update, context)


def movie(update: Update, context: CallbackContext) -> None:
    """Function for /movie command. It suggests an interesting movie for user"""
    pass


def series(update: Update, context: CallbackContext) -> None:
    """Function for /series command. It suggests an interesting TV series for user"""
    pass


def message_from_user(update: Update, context: CallbackContext) -> None:
    """Function for replying to user, which sent any message to this bot"""

    # Send "I don't understand you" message
    update.message.reply_text("I don't understand you!")

    # Send "Cry" sticker
    update.message.reply_sticker("CAACAgIAAxkBAAIBj2Dmz9_eF73lcpR-3VVjXf0kytVdAAJhAAN4qOYPf6tqRsGZTcYgBA")

    # Show help message
    help(update, context)


def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('movie', movie))
    dp.add_handler(CommandHandler('series', movie))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.all, message_from_user))

    # Run the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

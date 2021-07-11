#!/usr/bin/env python3

from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CallbackContext,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

import secret_token
import imdb_parser
import logging


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


def start(update: Update, context: CallbackContext) -> None:
    """Function for /start command"""

    # Send "Hello" sticker
    update.message.reply_sticker("CAACAgIAAxkBAAIBdWDmwUbnbcGuw7gMeJ_JF7QQq0uaAAKZDAACP1QBSs-TDHlrwSKUIAQ")

    # Show help message
    help(update, context)


def movie(update: Update, context: CallbackContext) -> None:
    """Function for /movie command. It suggests an interesting movie for user"""

    bot = context.bot
    chat_id = update.effective_chat.id

    movie = imdb_parser.get_movie()

    # Send info about the movie to user
    bot.send_message(
        chat_id,
        f"<b><u>Title</u></b>: {movie['title']}\n\n<b><u>Year</u></b>: {movie['year']}\n\n<b><u>Description</u></b>: {movie['description']}\n\n<b><u>Duration</u></b>: {movie['duration']}\n\n<b><u>Genre</u></b>: {movie['genre']}\n\n<b><u>IMDB rating</u></b>: {movie['rating']}",
        parse_mode=ParseMode.HTML
    )

    # Send movie poster to user
    bot.send_photo(chat_id, movie["poster"])

    # Create keyboard and send it to user
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("I like it", callback_data="like"),
            InlineKeyboardButton("Next", callback_data="next_movie"),
            InlineKeyboardButton("Stop", callback_data="stop")
        ],
    ])

    bot.send_message(chat_id, "Choose please:", reply_markup=keyboard)


def series(update: Update, context: CallbackContext) -> None:
    """Function for /series command. It suggests an interesting TV series for user"""
    pass


def button_clicked(update: Update, context: CallbackContext) -> None:
    """This function is called when user clicks on these buttons: 'I like it', 'Next', 'Stop'"""

    bot = context.bot
    chat_id = update.effective_chat.id
    data = update.callback_query.data

    if data == "like":
        # Send "Celebrate" sticker
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAICMmDpf7tQFdeTwBNOZqHPbuiVzgfeAAJiAAN4qOYPiW9skvfBcb8gBA")
    elif data == "next_movie":
        # Call movie() function
        movie(update, context)
    elif data == "next_series":
        # Call series() function
        series(update, context)
    elif data == "stop":
        # Send "Goodbye" sticker
        bot.send_sticker(chat_id, "CAACAgIAAxkBAAICM2DphV_KQa80OQt5ap0UCr9UbbNkAAJnCgAC7c-RSrGisn5sXFXpIAQ")

    # CallbackQueries need to be answered. See https://core.telegram.org/bots/api#callbackquery
    update.callback_query.answer()


def help(update: Update, context: CallbackContext) -> None:
    """Function for /help command"""

    # Send help message
    update.message.reply_text(
        "What can I do:\n\n  /start - say 'hello'\n\n  /movie - suggest an interesting movie\n\n  /series - suggest an interesting TV series\n\n  /help - show help message"
    )


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
    updater = Updater(secret_token.TOKEN)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('movie', movie))
    dp.add_handler(CommandHandler('series', movie))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CallbackQueryHandler(button_clicked))
    dp.add_handler(MessageHandler(Filters.all, message_from_user))

    # Run the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

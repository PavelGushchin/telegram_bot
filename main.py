#!/usr/bin/env python3

from telegram import (
    Update,
    ParseMode,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Updater,
    CallbackContext,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
)
from uuid import uuid4

import secret_token
import imdb_parser
import logging


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Function for '/start' command"""

    # Send "Hello" sticker
    update.message.reply_sticker("CAACAgIAAxkBAAIBdWDmwUbnbcGuw7gMeJ_JF7QQq0uaAAKZDAACP1QBSs-TDHlrwSKUIAQ")

    # Show help message
    help(update, context)


def movie(update: Update, context: CallbackContext) -> None:
    """Function for '/movie' command"""

    bot = context.bot
    chat_id = update.effective_chat.id

    # Send the message, which indicates that our bot has started working
    bot.send_message(chat_id, "Wait a second...")

    # Parse IMDB "Top 250 Movies" page
    movie = imdb_parser.get_movie()

    # Send information about chosen movie to the user
    bot.send_message(
        chat_id,
        f"<b><u>Title</u></b>: {movie['title']}\n\n"
        f"<b><u>Year</u></b>: {movie['year']}\n\n"
        f"<b><u>Description</u></b>: {movie['description']}\n\n"
        f"<b><u>Duration</u></b>: {movie['duration']}\n\n"
        f"<b><u>Genre</u></b>: {movie['genre']}\n\n"
        f"<b><u>IMDB rating</u></b>: {movie['rating']}",
        parse_mode=ParseMode.HTML
    )

    # Send movie poster to the user
    bot.send_photo(chat_id, movie["poster"])

    # Create keyboard and send it to the user
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("I like it", callback_data="like"),
            InlineKeyboardButton("Next", callback_data="next_movie"),
            InlineKeyboardButton("Stop", callback_data="stop")
        ],
    ])

    bot.send_message(chat_id, "Choose please:", reply_markup=keyboard)


def series(update: Update, context: CallbackContext) -> None:
    """Function for '/series' command"""

    bot = context.bot
    chat_id = update.effective_chat.id

    # Send the message, which indicates that our bot has started working
    bot.send_message(chat_id, "Wait a second...")

    # Parse IMDB "Top 250 Series" page
    series = imdb_parser.get_series()

    # Send information about chosen movie to the user
    bot.send_message(
        chat_id,
        f"<b><u>Title</u></b>: {series['title']}\n\n"
        f"<b><u>Year</u></b>: {series['year']}\n\n"
        f"<b><u>Description</u></b>: {series['description']}\n\n"
        f"<b><u>Genre</u></b>: {series['genre']}\n\n"
        f"<b><u>IMDB rating</u></b>: {series['rating']}",
        parse_mode=ParseMode.HTML
    )

    # Send series poster to the user
    bot.send_photo(chat_id, series["poster"])

    # Create keyboard and send it to the user
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("I like it", callback_data="like"),
            InlineKeyboardButton("Next", callback_data="next_series"),
            InlineKeyboardButton("Stop", callback_data="stop")
        ],
    ])

    bot.send_message(chat_id, "Choose please:", reply_markup=keyboard)


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
    """Function for '/help' command"""

    # Send help message
    update.message.reply_text(
        f"What can I do:\n\n"
        f"  /start - say 'hello'\n\n"
        f"  /movie - recommend an interesting movie\n\n"
        f"  /series - recommend an interesting TV series\n\n"
        f"  /help - show help message"
    )


def message_from_user(update: Update, context: CallbackContext) -> None:
    """Function for replying to user who sent a message to this bot"""

    # Send "I don't understand you" message
    update.message.reply_text("I don't understand you!")

    # Send "Cry" sticker
    update.message.reply_sticker("CAACAgIAAxkBAAIBj2Dmz9_eF73lcpR-3VVjXf0kytVdAAJhAAN4qOYPf6tqRsGZTcYgBA")

    # Show help message
    help(update, context)


def inline(update: Update, context: CallbackContext) -> None:
    """Function for handling inline queries from user"""

    random_movie = imdb_parser.choose_randomly(imdb_parser.TOP_250_MOVIES_LIST)
    random_series = imdb_parser.choose_randomly(imdb_parser.TOP_250_SERIES_LIST)

    context.bot.answer_inline_query(
        update.inline_query.id,
        [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Suggest a movie",
                input_message_content=InputTextMessageContent(random_movie["url"])
            ),
            InlineQueryResultArticle(
                id=str(uuid4()),
                title="Suggest a TV series",
                input_message_content=InputTextMessageContent(random_series["url"])
            ),
        ]
    )


def error(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the user"""
    logger.error(msg="Bot's error:", exc_info=context.error)

    # Send "Scared" sticker
    context.bot.send_sticker(
        update.effective_chat.id,
        "CAACAgIAAxkBAAICuGDr-Dq3lbUolukRs6F46IUMsqE4AAJ7DQACK-uISrOE001rp6qDIAQ"
    )

    # Send a message to the user about this error
    context.bot.send_message(
        update.effective_chat.id,
        "Something went wrong... An error occurred!"
    )


def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(secret_token.TOKEN)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('movie', movie))
    dp.add_handler(CommandHandler('series', series))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CallbackQueryHandler(button_clicked))
    dp.add_handler(MessageHandler(Filters.all, message_from_user))
    dp.add_handler(InlineQueryHandler(inline))
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

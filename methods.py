from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ChatAction, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging

logger = logging.getLogger(__name__)
OPTION = range(1)
information = []

def start(update: Update, _:CallbackContext):
    #Request for postal code
    update.message.reply_text("Please enter your postal code: ", reply_markup=ReplyKeyboardRemove())
    return OPTION


def display_or_add(update: Update, _:CallbackContext):
    #logger displays previous information entered, in this case Postal Code. Adds to an array
    user = update.message.from_user
    information.append(update.message.text)
    logger.info("Address of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['Submit a request', 'View volunteering opportunities']]
    update.message.reply_text("What would you like to do today?", reply_markup= ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'You have quit the conversation. Have a great day!'
    )
    return ConversationHandler.END
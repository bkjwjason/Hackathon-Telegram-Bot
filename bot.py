from faulthandler import cancel_dump_traceback_later
from setuptools import Command
import logging
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ChatAction, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
information = []
OPTION = range(1)
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
    update.message.reply_text("What would you like to do today?", reply_markup= ReplyKeyboardMarkup(reply_keyboard))
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'You have quit the conversation. Have a great day!'
    )
    return ConversationHandler.END







def main() -> None:
    # Start bot
    TOKEN = "5553340518:AAHPPct5kqRZ62BXWRCj8_2u9EZnQzKA2tE"
    bot = telegram.Bot(token=TOKEN)
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    start_conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)], 
    states = {OPTION: [MessageHandler(Filters.text, display_or_add)]}, 
    fallbacks=[CommandHandler('cancel', cancel)])
    dispatcher.add_handler(start_conv_handler)
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    updater.start_polling()
if __name__ == '__main__':
    main()
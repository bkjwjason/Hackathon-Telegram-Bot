from faulthandler import cancel_dump_traceback_later
from setuptools import Command
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
import methods 


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def main() -> None:
    # Start bot
    TOKEN = "5553340518:AAHPPct5kqRZ62BXWRCj8_2u9EZnQzKA2tE"

    bot = telegram.Bot(token=TOKEN)

    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    start_conv_handler = ConversationHandler(
                            entry_points=[CommandHandler('start', methods.start)], 

                            states = {methods.OPTION: [MessageHandler(Filters.text, methods.display_or_add)]},

                            fallbacks=[CommandHandler('cancel', methods.cancel)])

    dispatcher.add_handler(start_conv_handler)

    dispatcher.add_handler(CommandHandler('cancel', methods.cancel))

    updater.start_polling()
if __name__ == '__main__':
    main()
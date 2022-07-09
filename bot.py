from cgitb import text
from faulthandler import cancel_dump_traceback_later
from setuptools import Command
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, CallbackQueryHandler
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

                            states = {
                                methods.OPTION: [MessageHandler(Filters.text, methods.display_or_add)],
                                methods.PATH: [MessageHandler(Filters.text, methods.path)],
                                methods.STATE: [MessageHandler(Filters.text, methods.state)],
                                methods.UPDATE_NAME: [MessageHandler(Filters.text, methods.update_name)],
                                methods.UPDATE_NUMBER: [MessageHandler(Filters.text, methods.update_number)],
                                methods.UPDATE_DESC: [MessageHandler(Filters.text, methods.update_desc)],
                                methods.KEYBOARD : [MessageHandler(Filters.text, methods.keyboard)],
                                methods.SHOW_DATA: [MessageHandler(Filters.text, methods.show_data)]
                            },

                            fallbacks=[CommandHandler('cancel', methods.cancel)])

    dispatcher.add_handler(start_conv_handler)
    dispatcher.add_handler(CommandHandler('cancel', methods.cancel))

    updater.start_polling()
if __name__ == '__main__':
    main()
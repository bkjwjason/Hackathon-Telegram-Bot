from telegram.ext import Updater, CommandHandler
import logging
import methods 


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def main() -> None:
    # Start bot
    TOKEN = "TOKEN"
    updater = Updater(TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(methods.start_conv_handler)
    dispatcher.add_handler(CommandHandler('cancel', methods.cancel))
    updater.start_polling()

if __name__ == '__main__':
    main()
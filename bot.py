from telegram.ext import Updater, CommandHandler
import logging
import methods 
import os

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def main() -> None:
    # Start bot
    TOKEN = "TOKEN"
    updater = Updater(TOKEN)
    PORT = int(os.environ.get('PORT', '8443'))
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(methods.start_conv_handler)
    dispatcher.add_handler(CommandHandler('cancel', methods.cancel))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,webhook_url= 'https://hackathon-tele-bot.herokuapp.com/' + TOKEN)

if __name__ == '__main__':
    main()
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from database import getJobs, pushJob
import logging

logger = logging.getLogger(__name__)
OPTION, PATH, STATUS, UPDATE_NAME, UPDATE_NUMBER, UPDATE_DESC, UPDATE_CATEGORY,UPDATE_POSTAL, KEYBOARD, SHOW_DATA, DONE, DISTANCE  = range(12)
information = {}
chatid = None

def start(update: Update, _:CallbackContext):
    #Request for postal code
    update.message.reply_text("Please enter your postal code: ""\nTo quit, please type /cancel")
    global chatid
    chatid = update.message.chat_id
    return OPTION

def display_or_add(update: Update, _:CallbackContext):
    #logger displays previous information entered, in this case Postal Code. Adds to an array
    user = update.message.from_user
    information["Postal Code"] = int(update.message.text)
    logger.info("Address of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['😀Submit a request😀', '🧐View volunteering opportunities🧐']]
    update.message.reply_text("What would you like to do today?" "\nTo quit, please type /cancel", reply_markup= ReplyKeyboardMarkup(reply_keyboard))
    return PATH

def path(update: Update, _:CallbackContext):
    if update.message.text == "😀Submit a request😀":
        return keyboard()
    else:
        #insert the listing code here
        reply_keyboard = [[2, 4]]
        update.message.reply_text("Please choose your desired radius (in km)." "\nTo quit, please type /cancel", reply_markup = ReplyKeyboardMarkup(reply_keyboard))
        return DISTANCE

def show_jobs(update: Update, _:CallbackContext):
    distance = update.message.text
    res = getJobs(information["Postal Code"], int(distance), None)
    if res == False:
        update.message.reply_text("There are currently zero jobs available. Please look again another time. To restart the conversation, please type /start.", reply_markup = ReplyKeyboardRemove())
        return ConversationHandler.END
    update.message.reply_text("Here are some available jobs you can help volunteer for!", reply_markup = ReplyKeyboardRemove())
    ans = ""
    for item in res:
        temp = ""
        for key, value in item.items():
            temp = temp + key + ": " + str(value) + '\n'
        ans = ans + temp + '\n\n'
    update.message.reply_text(ans)
    update.message.reply_text("To restart the conversation, please type /start.")
    return ConversationHandler.END


def keyboard():
    print(information)
    msg= ("You may choose to add your name, phone number, category of work or the description of work. "
    "\nTo quit, please type /cancel")
    reply_keyboard = [["Name 😃", "Category 📃"], ["Description 📑", "Phone Number 📞"], ["Postal Code 🏠" , "Done 👍"]]
    bot.sendMessage(chat_id = chatid, text = msg, reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return STATUS

def status(update: Update, _:CallbackContext):
    if update.message.text == "Name 😃":
        update.message.reply_text("Please enter your name.", reply_markup = ReplyKeyboardRemove())
        return UPDATE_NAME
    elif update.message.text == "Category 📃":
        reply_keyboard = [["Renovation 🔨", "Gardening 🌱"],["Manual Labour 👷", "Necessities 🥗"]]
        update.message.reply_text("Please choose a category of your request.", reply_markup=ReplyKeyboardMarkup(reply_keyboard))
        return UPDATE_CATEGORY
    elif update.message.text == "Description 📑":
        update.message.reply_text("Please enter a short description of the request.",reply_markup = ReplyKeyboardRemove())
        return UPDATE_DESC
    elif update.message.text == "Phone Number 📞":
        update.message.reply_text("Please enter your phone number.",reply_markup = ReplyKeyboardRemove() )
        return UPDATE_NUMBER
    elif update.message.text == "Postal Code 🏠":
        update.message.reply_text("Please update your postal code.", reply_markup = ReplyKeyboardRemove() )
        return UPDATE_POSTAL
    elif update.message.text == "Done 👍":
        return show_data()

def update_name(update: Update, _:CallbackContext):
    information["Name"] = update.message.text
    return keyboard()

def update_number(update: Update, _:CallbackContext):
    information["Phone Number"] = int(update.message.text)
    return keyboard()

def update_desc(update: Update, _:CallbackContext):
    information["Description"] = update.message.text
    return keyboard()

def update_categories(update: Update, _:CallbackContext):
    information["Category"] = update.message.text
    return keyboard()

def update_postal(update: Update, _:CallbackContext):
    information["Postal Code"] = int(update.message.text)
    return keyboard()

def show_data():
    data = ""
    for key, value in information.items():
        data = data + key + ": " + str(value) + '\n'
    bot.send_message(chat_id = chatid, text = "Please check that the information is correct:" + "\n" + data)
    reply_keyboard = [["Yes", "No"]]
    bot.send_message(chat_id = chatid, text = "Would you like to submit?", reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return DONE

def done(update: Update, _: CallbackContext):
    if update.message.text == "Yes":
        pushJob(information)
        update.message.reply_text("Your request for help has been submitted! To add another request or view other requests, please type /start.", reply_markup = ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        return keyboard()

def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'You have quit the conversation. Have a great day!', reply_markup = ReplyKeyboardRemove()
    )
    return ConversationHandler.END


start_conv_handler = ConversationHandler(
                        entry_points=[CommandHandler('start', start)], 

                        states = {
                            OPTION: [MessageHandler(Filters.text & (~Filters.command), display_or_add)],
                            PATH: [MessageHandler(Filters.text & (~Filters.command), path)],
                            STATUS: [MessageHandler(Filters.text & (~Filters.command), status)],
                            UPDATE_NAME: [MessageHandler(Filters.text & (~Filters.command), update_name)],
                            UPDATE_NUMBER: [MessageHandler(Filters.text & (~Filters.command), update_number)],
                            UPDATE_CATEGORY: [MessageHandler(Filters.text & (~Filters.command), update_categories)],
                            UPDATE_DESC: [MessageHandler(Filters.text & (~Filters.command), update_desc)],
                            UPDATE_POSTAL: [MessageHandler(Filters.text & (~Filters.command), update_postal)], 
                            DONE: [MessageHandler(Filters.text & (~Filters.command), done)],
                            DISTANCE: [MessageHandler(Filters.text & (~Filters.command), show_jobs)]
                        },
                        fallbacks=[CommandHandler('cancel', cancel)])

bot = Bot("TOKEN")
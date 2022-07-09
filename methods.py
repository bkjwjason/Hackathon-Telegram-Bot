from email import message
import telegram
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ChatAction, User
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from database import pushJob
import logging

logger = logging.getLogger(__name__)
OPTION, PATH, STATE, VIEW, NAME, UPDATE_NAME, UPDATE_NUMBER, UPDATE_DESC, KEYBOARD, SHOW_DATA, DONE  = range(11)
information = {"Name": None, "Postal":None, "Desc": None, "Category":None}


def start(update: Update, _:CallbackContext):
    #Request for postal code
    update.message.reply_text("Please enter your postal code: ", reply_markup=ReplyKeyboardRemove())
    return OPTION

def display_or_add(update: Update, _:CallbackContext):
    #logger displays previous information entered, in this case Postal Code. Adds to an array
    user = update.message.from_user
    information["Postal"] = update.message.text
    logger.info("Address of %s: %s", user.first_name, update.message.text)
    reply_keyboard = [['Submit a request', 'View volunteering opportunities']]
    update.message.reply_text("What would you like to do today?", reply_markup= ReplyKeyboardMarkup(reply_keyboard))
    return PATH

def path(update: Update, _:CallbackContext):
    if update.message.text == "Submit a request":
        msg= ("You may choose to add your name, phone number, category of work or the description of work. "
        "To quit, please type /cancel")
        reply_keyboard = [["Name", "Category"], ["Description", "Phone Number"], ["Done"]]
        update.message.reply_text(msg, reply_markup=reply_keyboard)
        return STATE

def keyboard(update: Update, _:CallbackContext):
    msg= ("You may choose to add your name, phone number, category of work or the description of work. "
    "To quit, please type /cancel")
    reply_keyboard = [["Name", "Category"], ["Description", "Phone Number"], ["Done"]]
    update.message.reply_text(msg, reply_markup=reply_keyboard)
    return STATE

def state(update: Update, _:CallbackContext):
    if update.message.text == "Name":
        update.message.reply_text("Please enter your name", reply_markup = ReplyKeyboardRemove)
        return UPDATE_NAME
    elif update.message.text == "Category":
        pass
    elif update.message.text == "Description":
        update.message.reply_text("Please enter a short description of the request",reply_markup = ReplyKeyboardRemove)
        return UPDATE_DESC
    elif update.message.text == "Phone Number":
        update.message.reply_text("Please enter your phone number")
        return UPDATE_NUMBER
    elif update.message.text == "Done":
        return SHOW_DATA

def update_name(update: Update, _:CallbackContext):
    information["Name"] = update.message.text
    return KEYBOARD

def update_number(update: Update, _:CallbackContext):
    information["Number"] = update.message.text
    return KEYBOARD

def update_desc(update: Update, _:CallbackContext):
    information["Desc"] = update.message.text
    return KEYBOARD

def update_categories(update: Update, _:CallbackContext):
    information["Category"] = update.message.text
    return KEYBOARD

def show_data(update: Update, _:CallbackContext):
    data = ""
    for key, value in information.items():
        data = data + key + ": " + value
    update.message.reply_text("Please check that the information is correct:" + "\n" + data)
    reply_keyboard = [["Yes", "No"]]
    update.message.reply_text("Would you like to submit?", reply_markup=reply_keyboard)
    return DONE
def categories(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()
    category_keys = [
        [
        InlineKeyboardButton(text = "Renovation", callback_data="Renovation"),
        InlineKeyboardButton(text = "Gardening", callback_data='Gardening')
        ],
        [   
        InlineKeyboardButton(text = "Manual Labour", callback_data='Manual Labour'),
        InlineKeyboardButton(text = "Necessities", callback_data= "Necessities")
        ],
    ]
    keyboard = InlineKeyboardMarkup(category_keys)
    query.edit_message_text("What kind of job is it?")
    query.edit_message_reply_markup(keyboard)

def done(update: Update, _: CallbackContext):
    if update.message.text == "Yes":
        pushJob(information)
        update.message.reply_text("Your request has been submitted. Have a great day!")
    else:
        return KEYBOARD

def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'You have quit the conversation. Have a great day!'
    )
    return ConversationHandler.END


bot = Bot("5553340518:AAHPPct5kqRZ62BXWRCj8_2u9EZnQzKA2tE")
import firebase_admin
import json
from firebase_admin import db
from distance import *

cred_obj = firebase_admin.credentials.Certificate(
    "help-a-neighbour-out-firebase-adminsdk-3k1ih-a01592b112.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://help-a-neighbour-out-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference("/tasks")

# user adds single task onto Firebase
def pushTask(taskObj):
    ref.push().set(taskObj)

# retrieves all tasks that falls within the user's selected range
def retrieveTasks(userPostal, selectedRange):
    filteredTasks = []
    allTasks = ref.get()
    # for taskObj in allTasks.values():


x = {
    "Postal": 738081,
    "Phone Number": 91141536,
    "Name": "Rayner Toh",
    "Category": "Gardening",
    "Desc": "Suck my balls"
}

print(calculate_distance(738081, 821308));
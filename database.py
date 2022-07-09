import firebase_admin
import json
from firebase_admin import db
from distance import *

cred_obj = firebase_admin.credentials.Certificate(
    "help-a-neighbour-out-firebase-adminsdk-3k1ih-a01592b112.json")
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': 'https://help-a-neighbour-out-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

jobsRef = db.reference("/jobs")

# pushes single job onto Firebase
def pushJob(jobObj):
    jobsRef.push().set(jobObj)

# retrieves all jobs that falls within the user's selected range
def getJobs(userPostal, selectedRange, selectedCategory):
    filteredJobs = []
    allJobs = jobsRef.get()
    if allJobs == None:
        return False
    for jobObj in allJobs.values():
        dist = calculate_distance(userPostal, jobObj['Postal Code'])
        if dist <= selectedRange:
            filteredJobs.append(jobObj)
    if filteredJobs == []:
        return False
    return filteredJobs

        


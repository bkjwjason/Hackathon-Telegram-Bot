#  to calculate distance based on postal code

import math
import pandas


def convert_to_geo(postal_code):

    data = pandas.read_csv('updated data.csv')  # postal code data for Singapore
    relevant = data[data['postal code'] == int(postal_code)]  # remove zero padding
    return math.radians(relevant['latitude'].item()), math.radians(relevant['longitude'].item())


def calculate_distance(postal_code_1, postal_code_2):
    lat1, long1 = convert_to_geo(postal_code_1)
    lat2, long2 = convert_to_geo(postal_code_2)
    res = 3963.0 * math.acos((math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)))
    return res * 1.609 # return distance in km



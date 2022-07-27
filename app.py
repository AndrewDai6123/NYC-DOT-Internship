import pandas as pd
import requests
import json

df = pd.read_csv("accessible-pedestrian-signals.csv")
pd.set_option('display.max_rows', None)

'''To-Do: automate this process with for-loop to read from csv file and print retrieved data to new csv file'''
parameters = {
    "Borough": "3",
    "Street1": "10th Avenue",
    "Borough2": "3",
    "Street2": "73rd Street",
    "Key": "",
}

response = requests.get("https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_2?", params=parameters)
print(response.text)

'''
Borough: 1 = Manhattan, 2 = Bronx, 3 = Brooklyn, 4 = Queens, 5 = Statin Island

https://geoservice.planning.nyc.gov/
Functions 1A, 1B, 1E, AP parameters:
"Borough": "1",
"AddressNo": "120",
"StreetName": "bwy",
"Key": "fAAdUpAeZcHg0AQ7",

Function 2 parameters
"Borough": "3",
"Street1": "10th Avenue",
"Borough2": "3",
"Street2": "73rd Street",
"Key": "",
'''
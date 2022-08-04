from lib2to3.pgen2 import driver
import pandas as pd
import requests
import json
import csv
import geopandas as gpd


#Read accessible-pedestrian-signals csv
df = pd.read_csv("accessible-pedestrian-signals.csv")
pd.set_option('display.max_rows', None)

'''Notes
Function 2: "and" and "at"
Function 3: "between, and" and "with, and" '''
# Global Variables
Key = "fAAdUpAeZcHg0AQ7"
Function2url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_2?"
Function3url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_3?"

#Geocoding
for i, row in df.iterrows():
    #Variables
    Borough = str(df.at[i,'Borough'])
    F2Str1 = str(df.at[i,'Location']).rpartition('and')[0]
    F2Str2 = str(df.at[i,'Location']).rpartition('and')[2]
    OnStr = str(df.at[i,'Location']).rpartition('between')[0]
    FromStr = str(df.at[i,'Location'])[str(df.at[i,'Location']).find("between")+len("between"):str(df.at[i,'Location']).rfind("and")]
    ToStr = str(df.at[i,'Location']).rpartition('and')[2]
    #For memory reasons, we will only be going through the first couple of addresses
    if i == 3:
        break

    if "between" or "with" not in str(df.at[i,'Location']):
        try: 
            parameters = {
            "Borough1": Borough,
            "Street1": F2Str1,
            "Borough2": Borough,
            "Street2": F2Str2,
            "Borough3": Borough,
            "Key": Key,
            }
            
            response = requests.get(Function2url, params=parameters)
            data = json.loads(response.text)
            print(data)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))
    
    if "between" in str(df.at[i,'Location']):
        try:
            parameters = {
            "Borough1": Borough,
            "OnStreet": OnStr,
            "SecondCrossStreet": ToStr,
            "Borough2": Borough,
            "FirstCrossStreet": FromStr,
            "Borough3": Borough,
            "Key": Key,
            }

            response = requests.get(Function3url, params=parameters)
            data = json.loads(response.text)
            print(data)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))
    
    if "with" in str(df.at[i,'Location']):
        try:
            parameters = {
            "Borough1": Borough,
            "OnStreet": OnStr,
            "SecondCrossStreet": ToStr,
            "Borough2": Borough,
            "FirstCrossStreet": FromStr,
            "Borough3": Borough,
            "Key": Key,
            }

            response = requests.get(Function3url, params=parameters)
            data = json.loads(response.text)
            print(data)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))


#Save data to csv file
df.to_csv('accessible-pedestrian-signals-Geo.csv')


#Notes
'''
Borough: 1 = Manhattan, 2 = Bronx, 3 = Brooklyn, 4 = Queens, 5 = Statin Island

https://geoservice.planning.nyc.gov/
Functions 1A, 1B, 1E, AP parameters:
"Borough": "1",
"AddressNo": "120",
"StreetName": "bwy",
"Key": "",

Function 2 parameters
"Borough": "3",
"Street1": "10th Avenue",
"Borough2": "3",
"Street2": "73rd Street",
"Key": "",

Function 3 parameters
"Borough1": "1",
"OnStreet": "bwy",
"SecondCrossStreet": "cedar",
"Borough2": "1",
"FirstCrossStreet": "thames",
"Borough3": "1",
"Key": "",

#Test Function 3
parameters = {
    "Borough1": "1",
    "OnStreet": "bwy",
    "SecondCrossStreet": "cedar",
    "Borough2": "1",
    "FirstCrossStreet": "thames",
    "Borough3": "1",
    "Key": "",
    }

response = requests.get("https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_3?", params=parameters)
print(response.text)

#Test Function 1B
parameters = {
    "Borough": str(df.at[i,'Borough']),
    "AddressNo": str(df.at[i,'Location'])[str(df.at[i,'Location']).find(start)+len(start):str(df.at[i,'Location']).rfind(AddressNo_end)],
    "StreetName": str(df.at[i,'Location'])[str(df.at[i,'Location']).find(start)+len(start):str(df.at[i,'Location']).rfind(Location_end)],
    "Key": "",
    }
    print(parameters)
'''
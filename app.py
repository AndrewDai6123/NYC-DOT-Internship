import pandas as pd
import requests
import json

#Read accessible-pedestrian-signals csv
df = pd.read_csv("accessible-pedestrian-signals.csv")
pd.set_option('display.max_rows', None)

#API Variables
Key = "fAAdUpAeZcHg0AQ7"
Function2url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_2?"
Function3url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_3?"

#Geocoding
for i, row in df.iterrows():
    #Geo Variables
    Borough = str(df.at[i,'Borough'])
    #Function 2 "and" or "at"
    F2Str1 = str(df.at[i,'Location']).rpartition(' and ' or ' at ')[0]
    F2Str2 = str(df.at[i,'Location']).rpartition(' and ' or ' at ')[2]
    #Function 3 "between, and"
    OnStrB = str(df.at[i,'Location']).rpartition(' between ')[0]
    FromStrB = str(df.at[i,'Location'])[str(df.at[i,'Location']).find(" between ")+len(" between "):str(df.at[i,'Location']).rfind(" and ")]
    ToStrB = str(df.at[i,'Location']).rpartition(' and ')[2]
    #Function 3 "with, and"
    OnStrW = str(df.at[i,'Location']).rpartition(' with ')[0]
    FromStrW = str(df.at[i,'Location'])[str(df.at[i,'Location']).find(" with ")+len(" with "):str(df.at[i,'Location']).rfind(" and ")]
    ToStrW = str(df.at[i,'Location']).rpartition(' and ')[2]

    # Small Test for memory and time reasons
    #if i == 3:
        #break

    #Function 2 for intersect locations with "and" or "at"
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

            data = json.loads(response.text)['display']
            lat = (data['out_latitude'])
            lng = (data['out_longitude'])
            df.at[i, 'lat'] = lat
            df.at[i, 'lng'] = lng
            print(i, lat, lng)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))

    
    #Function 3 on, from, to: locations with "between" and "and"
    if "between" in str(df.at[i,'Location']):
        try:
            parameters = {
            "Borough1": Borough,
            "OnStreet": OnStrB,
            "SecondCrossStreet": ToStrB,
            "Borough2": Borough,
            "FirstCrossStreet": FromStrB,
            "Borough3": Borough,
            "Key": Key,
            }

            response = requests.get(Function3url, params=parameters)

            data = json.loads(response.text)['display']
            from_lat = (data['out_from_latitude'])
            from_lng = (data['out_from_longitude'])
            df.at[i, 'from_lat'] = from_lat
            df.at[i, 'from_lng'] = from_lng
            to_lat = (data['out_to_latitude'])
            to_lng = (data['out_to_longitude'])
            df.at[i, 'to_lat'] = to_lat
            df.at[i, 'to_lng'] = to_lng
            print(i, from_lat, from_lng, to_lat, to_lng)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))

    #Function 3 on, from, to: locations with "with" and "and"
    if "with" in str(df.at[i,'Location']):
        try:
            parameters = {
            "Borough1": Borough,
            "OnStreet": OnStrW,
            "SecondCrossStreet": ToStrW,
            "Borough2": Borough,
            "FirstCrossStreet": FromStrW,
            "Borough3": Borough,
            "Key": Key,
            }

            response = requests.get(Function3url, params=parameters)

            data = json.loads(response.text)['display']
            from_lat = (data['out_from_latitude'])
            from_lng = (data['out_from_longitude'])
            df.at[i, 'from_lat'] = from_lat
            df.at[i, 'from_lng'] = from_lng
            to_lat = (data['out_to_latitude'])
            to_lng = (data['out_to_longitude'])
            df.at[i, 'to_lat'] = to_lat
            df.at[i, 'to_lng'] = to_lng
            print(i, from_lat, from_lng, to_lat, to_lng)
        except:
            print('Not geocoded: ' + str(df.at[i,'Location']))


#Save data to csv file
df.to_csv('accessible-pedestrian-signals-Geo.csv')

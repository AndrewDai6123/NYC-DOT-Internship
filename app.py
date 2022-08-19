import pandas as pd
import requests
import json
import geopandas as gpd
from shapely.geometry import LineString, Point

#Read accessible-pedestrian-signals csv
df = pd.read_csv("input files/accessible-pedestrian-signals.csv")
pd.set_option('display.max_rows', None)
errorLog = {"LineNumber": [], 'Location': [], "Borough": [], "Errors": []}

#API Variables
Key = "fAAdUpAeZcHg0AQ7"
Function2url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_2?"
Function3url = "https://geoservice.planning.nyc.gov/geoservice/geoservice.svc/Function_3?"

#Geocoding
for i, row in df.iterrows():
    #Geo Variables
    address = str(df.at[i, 'Location'])
    Borough = str(df.at[i,'Borough'])
    #Function 2 "and"
    F2Str1and = str(df.at[i,'Location']).rpartition(' and ')[0]
    F2Str2and = str(df.at[i,'Location']).rpartition(' and ')[2]
    #Function 2 "at"
    F2Str1at = str(df.at[i,'Location']).rpartition(' at ')[0]
    F2Str2at = str(df.at[i,'Location']).rpartition(' at ')[2]
    #Function 3 "between, and"
    OnStrB = str(df.at[i,'Location']).rpartition(' between ')[0]
    FromStrB = str(df.at[i,'Location'])[str(df.at[i,'Location']).find(" between ")+len(" between "):str(df.at[i,'Location']).rfind(" and ")]
    ToStrB = str(df.at[i,'Location']).rpartition(' and ')[2]
    #Function 3 "with, and"
    OnStrW = str(df.at[i,'Location']).rpartition(' with ')[0]
    FromStrW = str(df.at[i,'Location'])[str(df.at[i,'Location']).find(" with ")+len(" with "):str(df.at[i,'Location']).rfind(" and ")]
    ToStrW = str(df.at[i,'Location']).rpartition(' and ')[2]

    # Small Test for memory and time reasons
    # if i == 8:
    #     break
    
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
            jData = pd.json_normalize(data)
            #(long, lat)
            p1 = float(data['out_from_longitude']), float(data['out_from_latitude'])
            p2 = float(data['out_to_longitude']), float(data['out_to_latitude'])
            line = LineString([p1, p2])
            header = iter(jData.keys())
            values = data.values()
            df.at[i, 'geometry'] = line
            df.at[i, header] = values
            print(i, str(df.at[i,'Location']), line)
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']) + " " + data["out_error_message"])
            errorLog["LineNumber"].append(i)
            errorLog["Location"].append(address)
            errorLog["Borough"].append(Borough)
            errorLog["Errors"].append(data["out_error_message"])
            df.at[i, 'out_error_message'] = data['out_error_message']


    #Function 3 on, from, to: locations with "with" and "and"
    elif "with" in str(df.at[i,'Location']):
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
            jData = pd.json_normalize(data)
            #(long, lat)
            p1 = float(data['out_from_longitude']), float(data['out_from_latitude'])
            p2 = float(data['out_to_longitude']), float(data['out_to_latitude'])
            line = LineString(p1, p2)
            header = iter(jData.keys())
            values = data.values()
            df.at[i, 'geometry'] = line
            df.at[i, header] = values
            print(i, str(df.at[i,'Location']), line)
        except:
            print('Not geocoded: ' + str(df.at[i, 'Location']) + " " + data["out_error_message"])
            errorLog["LineNumber"].append(i)
            errorLog["Location"].append(address)
            errorLog["Borough"].append(Borough)
            errorLog["Errors"].append(data["out_error_message"])
            df.at[i, 'out_error_message'] = data['out_error_message']


    #Function 2 for intersect locations with "at"
    elif " at " in str(df.at[i,'Location']):
        try: 
            parameters = {
            "Borough1": Borough,
            "Street1": F2Str1at,
            "Borough2": Borough,
            "Street2": F2Str2at,
            "Borough3": Borough,
            "Key": Key,
            }
            
            response = requests.get(Function2url, params=parameters)

            data = json.loads(response.text)['display']
            jData = pd.json_normalize(data)
            p1 = float(data['out_latitude'])
            p2 = float(data['out_longitude'])
            #(long, Lat)
            point = Point(p2, p1)
            header = iter(jData.keys())
            values = data.values()
            df.at[i, 'geometry'] = str(point)
            df.at[i, header] = values
            print(i, str(df.at[i,'Location']), point)
        except Exception as e:
            print('Not geocoded: ' + str(df.at[i, 'Location']) + " " + data["out_error_message"])
            errorLog["LineNumber"].append(i)
            errorLog["Location"].append(address)
            errorLog["Borough"].append(Borough)
            errorLog["Errors"].append(data["out_error_message"])
            df.at[i, 'out_error_message'] = data['out_error_message']


    
    #Function 2 for intersect locations with "and"
    elif " and " in str(df.at[i,'Location']):
        try: 
            parameters = {
            "Borough1": Borough,
            "Street1": F2Str1and,
            "Borough2": Borough,
            "Street2": F2Str2and,
            "Borough3": Borough,
            "Key": Key,
            }
            
            response = requests.get(Function2url, params=parameters)

            data = json.loads(response.text)['display']
            jData = pd.json_normalize(data)
            p1 = float(data['out_latitude'])
            p2 = float(data['out_longitude'])
            #(long, Lat)
            point = Point(p2, p1)
            header = iter(jData.keys())
            values = data.values()
            df.at[i, 'geometry'] = str(point)
            df.at[i, header] = values
            print(i, str(df.at[i,'Location']), point)
        except Exception as e:
            print('Not geocoded: ' + str(df.at[i, 'Location']) + " " + data["out_error_message"])
            errorLog["LineNumber"].append(i)
            errorLog["Location"].append(address)
            errorLog["Borough"].append(Borough)
            errorLog["Errors"].append(data["out_error_message"])
            df.at[i, 'out_error_message'] = data['out_error_message']

errorLogDF = pd.DataFrame(errorLog)
errorLogDF.to_csv("output CSV files/ErrorLog.csv", index=False)
#Save data to csv file
df.to_csv('output CSV files/accessible-pedestrian-signals-Geo.csv')

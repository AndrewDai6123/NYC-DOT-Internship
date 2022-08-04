# NYC-DOT-Internship

API used: https://geoservice.planning.nyc.gov/
Borough codes for API parameters: 1 = Manhattan, 2 = Bronx, 3 = Brooklyn, 4 = Queens, 5 = Statin Island

Register for Geoservice API Key and enter it into the Key variable.

Some example API Function parameters - 
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
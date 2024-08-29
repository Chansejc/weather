from typing import Dict
import json
import datetime
import sys
import requests

VC_API_KEY = None
try: 
    with open("./.env.json", "r") as f:
        VC_API_KEY = json.loads(f.read())["VC_API_KEY"]
except Exception as e:
    print("Could not find API Key file")
    sys.exit()


#Exception used when the date found in the JSON is not the current date
class InvalidDate(Exception):
    pass

def get_current_date() -> str: return str(datetime.date.today())

#Checks to make sure that he date found in the JSON is the current date as the JSON may not always be correct
def check_date(data: Dict) -> bool: return data["datetime"] == get_current_date()

#Takes in a location Hash which will be used in a URL query for JSON on the locations weather 
def get_all_weather_data(location: Dict[str, str]) -> tuple[Dict[str, str] | None, Exception | None]:
    err = None
    try:
        URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/ \
                {location['lat']},{location['long']}?unitGroup=us&key={VC_API_KEY}"
        res = requests.get(URL)
        return (res.json(), err)
    except Exception as e:
        err = e
    return None, err

#Find matching object based on current date
def get_todays_data(data: Dict) -> tuple[Dict[str, str] | None, Exception | None]:
    err = None
    curData = data["days"][0]
    if not check_date(curData): 
        curData = None
        err = InvalidDate("Not using the correct date value issue with the server")
    return curData, err



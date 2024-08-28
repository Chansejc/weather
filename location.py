import geopy.geocoders
import sys
from typing import Dict

def get_location_by_city_state(state: str, city: str) -> tuple[Dict[str, str], None | Exception]:
    err = None
    location = {"":""}
    try:
        loc = geopy.geocoders.Nominatim(user_agent="app")

        cords = loc.geocode({"state": state, "city": city})
        if cords == None: 
            print("No latitude/longitude found")
            sys.exit()
        
        location = {
                "long": cords.longitude, 
                "lat": cords.latitude
                }
    except Exception as e:
        err = e
    finally:
        return (location, err)

def get_location_by_zipcode(zipcode: str) -> tuple[Dict, None | Exception]: #Only useful for USA unless there is a specifier for Country 
    err = None
    location: Dict[str, str] = {"": ""}
    try:
        loc = geopy.geocoders.Nominatim(user_agent="app")

        cords = loc.geocode({"country": "USA", "postalcode": zipcode})
        if cords == None:
            print("No latitude/longitude found")
            sys.exit()

        location = {
                "long": cords.longitude, 
                "lat": cords.latitude 
                }

    except Exception as e:
        err = e
    finally:
        return (location, err)


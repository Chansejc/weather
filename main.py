import query
import parser
import location
import sys

def main():
    loc, err = location.get_location_by_city_state(state="Texas", city="Grapevine")
    if err != None:
        print(err)
        sys.exit()

    data, err = query.get_all_weather_data(loc)
    if err != None or data == None: 
        print("Issue Getting All Weather Data", err)
        sys.exit()

    data, err = query.get_todays_data(data)
    if err: 
        print("Issue Getting Today's Weather Data", err)
        sys.exit()
        
    if data != None: 
        load = parser.PayloadParser(data)
        print(load.outlook)
    else: 
        print(Exception("Data returned a NoneType"))

if __name__ == "__main__":
    main()

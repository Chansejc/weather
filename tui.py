import simple_term_menu as stm
import sys
import query
import parser
import location



def tui():
    options = ["ZipCode", "City/State", "Quit"]
    menu = stm.TerminalMenu(
            options,
            ) 
    index = menu.show() 
    if type(index) != int:
        print("Error Getting index from key press")
        sys.exit()
    choice = options[index]
    
    match choice:
        case "ZipCode":
            zip = input("ZipCode: ")
            cords, err = location.get_location_by_zipcode(zip)
            if err != None or cords == None: 
                print("Error Getting Coordinates Possible Bad ZipCode", err)
                sys.exit()

            data, err = query.get_all_weather_data(cords)
            if err != None or data == None: 
                print("Error Getting All Weather Data", err)
                raise err
                sys.exit()

            data, err = query.get_todays_data(data)
            if err != None or data == None: 
                print("Error Getting Today's Weather Data", err)
                sys.exit()

            load = parser.PayloadParser(data)
            print(load.outlook)

        case "City/State":
            city = input("Enter City").strip(" ")
            state = input("Enter State").strip(" ")

            cords, err = location.get_location_by_city_state(state, city)
            if err != None or cords == None: 
                print("Error Getting Coordinates", err)
                sys.exit()

            data, err = query.get_all_weather_data(cords)
            if err != None or data == None: 
                print("Error Getting All Weather Data", err)
                sys.exit()

            data, err = query.get_todays_data(data)
            if err != None or data == None: 
                print("Error Getting Today's Weather Data", err)
                sys.exit()

            load = parser.PayloadParser(data)
            print(load.outlook)

        case "Quit":
            sys.exit() 

if __name__ == "__main__":
    tui()

from typing import Dict

class Code:
    def __init__(self, code) -> None:
        self.code: str = code 
        self.end = "\033[0m"

    def show(self, text): print( f"{self.code}{text}{self.end}" )
    def ret(self, text): return ( f"{self.code}{text}{self.end}" )

    
class EscCode:
    green = Code("\033[32m")
    red = Code("\033[31m")
    cyan = Code("\033[36m")
    yellow = Code("\033[33m")
    blue = Code("\033[34m")
    magenta = Code("\033[35m")

class Metric:
    count: int = 0
    total: float = 0

    def getAvr(self) -> int:
        return int(round(self.total / self.count, 2))

    def zero(self): 
        self.count = 0
        self.total = 0

class Forecast:
    feelslike: int
    temp: int
    windSpeed: int
    precipitation: float
    humidity: int

    def __repr__(self) -> str:
        return (
                f""" 
        {EscCode.blue.ret('Feels Like:')} {EscCode.green.ret(self.feelslike)}
        {EscCode.blue.ret('Temperature:')} {EscCode.green.ret(self.temp)}
        {EscCode.blue.ret('Winds:')} {EscCode.green.ret(self.windSpeed)}
        {EscCode.blue.ret('Precipitation:')} {EscCode.green.ret(self.precipitation)}
        {EscCode.blue.ret('Humidity:')} {EscCode.green.ret(self.humidity)}
                """
                )

class Outlook:
    moonPhase: str
    sunrise: str 
    sunset: str
    morning = Forecast()
    afternoon = Forecast()
    evening = Forecast()
    overnight = Forecast()

    def __repr__(self) -> str:
        return (
                f"""
            {EscCode.red.ret('Days Outlook:')}
            {EscCode.blue.ret('Sunrise:')}{EscCode.green.ret(self.sunrise)}
            {EscCode.blue.ret('Sunset:')}{EscCode.green.ret(self.sunset)}
            Morning: 
            -------
                {self.morning}
            Afternoon: 
            -------
                {self.afternoon}
            Evening: 
            -------
                {self.evening}
            Overnight: 
            -------
                {self.overnight}
                """
                )

class PayloadParser:
    def __init__(self, load: Dict):
        self.outlook = Outlook()
        self.temp = Metric()
        self.precipitations = Metric()
        self.humidities = Metric()
        self.windSpeeds = Metric()
        self.feelslikes = Metric()
        self.payload = load
        self.buildOutlook() 

    def addTemp(self, n: float) -> None: 
        self.temp.count += 1
        self.temp.total += n

    def addWindSpeed(self, n: float) -> None:
        self.windSpeeds.count += 1
        self.windSpeeds.total += n

    def addPrecipitation(self, n: float) -> None:
        self.precipitations.count += 1
        self.precipitations.total += n

    def addHumidities(self, n: float) -> None:
        self.humidities.count += 1
        self.humidities.total += n

    def addFeelslike(self, n: float) -> None:
        self.feelslikes.count += 1
        self.feelslikes.total += n

    def getAverages(self) -> Forecast:
        final = Forecast()
        final.temp = int(round(self.temp.total/self.temp.count, 2))
        final.windSpeed = int(round(self.windSpeeds.total/self.windSpeeds.count, 2))
        final.precipitation = int(round(self.precipitations.total/self.precipitations.count, 2))
        final.humidity = int(round(self.humidities.total/self.humidities.count, 2))
        return final

    def buildOutlook(self) -> None:
        self.outlook.sunset = self.payload["sunset"]
        self.outlook.sunrise = self.payload["sunrise"]
        hoursCount = 0
        while hoursCount < len(self.payload["hours"]):
            self.addHumidities(self.payload["hours"][hoursCount]["humidity"])
            self.addPrecipitation(self.payload["hours"][hoursCount]["precip"])
            self.addWindSpeed(self.payload["hours"][hoursCount]["windspeed"])
            self.addTemp(self.payload["hours"][hoursCount]["temp"])
            self.addFeelslike(self.payload["hours"][hoursCount]["feelslike"])
            match hoursCount:
                case 5: self.buildForecast(self.outlook.overnight)
                case 11: self.buildForecast(self.outlook.morning)
                case 16: self.buildForecast(self.outlook.afternoon)
                case 23: self.buildForecast(self.outlook.evening)
            hoursCount += 1

    def buildForecast(self, fore: Forecast):
        fore.humidity = self.humidities.getAvr()
        self.humidities.zero()
        fore.precipitation = self.precipitations.getAvr()
        self.precipitations.zero()
        fore.temp = self.temp.getAvr()
        self.temp.zero()
        fore.windSpeed = self.windSpeeds.getAvr()
        self.windSpeeds.zero()
        fore.feelslike = self.feelslikes.getAvr()
        self.feelslikes.zero()
                

"""
 Payload -> 
 {
       "1" -> Get Values and Counts for Metrics from each Time
       "2" -> Track Times and create object after last Time in Slot
       "3" -> Convert Metrics to Forecasts for said Timeslot
 }
* Serve Each time slot's Forecast *

[
  Moon Phase,
  Sunrise & Sunset Times,
  Morning (*6:00 - 11:00*): ,
  Afternoon ( *12:00 - 16:00* ): 
  Evening ( *17:00 - 23:00* ): 
  Overnight (*Next Day 01:00 - 05:00*):
]

+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+_+

Morning (*6:00 - 11:00*): {
Temp (AVG), [x]
Wind (MPH), [x]
Precipitation (AVG), [x]
Humidity (%), [x]
Feels Like Temp, [o]
},

"""


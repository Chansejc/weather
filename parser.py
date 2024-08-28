from typing import Dict
from tests import EscCodes as ec

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
        {ec.blue.ret('Feels Like:')} {ec.green.ret(self.feelslike)}
        {ec.blue.ret('Temperature:')} {ec.green.ret(self.temp)}
        {ec.blue.ret('Winds:')} {ec.green.ret(self.windSpeed)}
        {ec.blue.ret('Precipitation:')} {ec.green.ret(self.precipitation)}
        {ec.blue.ret('Humidity:')} {ec.green.ret(self.humidity)}
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
            {ec.red.ret('Days Outlook:')}
            {ec.blue.ret('Sunrise:')}{ec.green.ret(self.sunrise)}
            {ec.blue.ret('Sunset:')}{ec.green.ret(self.sunset)}
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


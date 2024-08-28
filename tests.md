#Location Tests
- ZipCodes | City, State/City, Province should return the same Coordinates
- Unknown locations should return an Exception

#Temperature Tests
- Averages should be rounded to the nearest integer
- Averages should be within 4 degrees of current temperature

#API
- Should return Error codes instead of JSON values for errors

#JSON
- Should include 
- [
    Morning Temp,
    Afternoon Temp,
    Evening Temp,
    Overnight Temp,
    Wind (mph),
    Precipication (percentage with meeter chart),
    Humidity (percentage with meeter chart),
    Feels Like Temp,
    Moon Phase,
    Sunrise & Sunset Times
 ]

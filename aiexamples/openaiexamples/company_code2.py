import pytz
import datetime

# a function to print the current date and time locally, in new york, and in london
def printTime():
    localTime = datetime.datetime.now()
    NYTime = datetime.datetime.now(pytz.timezone('America/New_York'))
    london_time = datetime.datetime.now(pytz.timezone('Europe/London'))
    print('Local time:', localTime)
    print('New York time:', NYTime)
    print('London time:', london_time)

printTime()

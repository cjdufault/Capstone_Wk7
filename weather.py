"""
Gets weather forecasts for a specified location.
Usage: python [path]/weather.py [location] [unit system]
"""

import requests
import os
import sys
from datetime import datetime


WEATHER_KEY = os.environ.get('WEATHER_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/forecast?'


def main():
    if WEATHER_KEY != None:
        args = get_args(2)
        
        location = args[0]
        units = args[1]
        
        # ask for input if location not entered
        if location == None:
            location = input('Enter location:  ')
        
        """I'm allowing more flexible location input from the user than
        'city, country code' because the API is able to handle somewhat
        ambiguous place names. This allows for searching for places with
        the same name as a much better known place, such as Minneapolis, Kansas
        ('q=minneapolis,ks,us' works for this), and searching for cities whose
        country is unknown to the user for whatever reason."""
            
        # use metric by default, api uses kelvin by default
        if units == None:
            units = 'metric'
            
        parameters = {'q': location, 'units': units, 'appid': WEATHER_KEY}
        response = requests.get(API_URL, params=parameters).json()
        
        if response['cod'] == '200':
            show_forecast(response['list'], units)
        else:
            print(response['message'])  # show message from api if code not 200
                
    else:
        print('No API key found. Set environment variable "WEATHER_KEY".')
        

def show_forecast(forecast_list, units):
    # specify what unit symbols should be used based on the unit system
    if units.lower() == 'metric':
        temp_unit = '°C'
        speed_unit = 'm/s'
    elif units.lower() == 'imperial':
        temp_unit = '°F'
        speed_unit = 'mph'
    else:
        temp_unit = 'K'
        speed_unit = 'm/s'
    
    for forecast in forecast_list:
        timestamp = forecast['dt']
        date = datetime.fromtimestamp(timestamp)
        
        temp = forecast['main']['temp']
        desc = forecast['weather'][0]['main']
        windspeed = forecast['wind']['speed']
        
        print(f'At {date}, {desc} and {temp}{temp_unit} with {windspeed} {speed_unit} winds')
        

# returns a list with a length equal to the number of expected arguments, with
# arguments that weren't entered represented as None
def get_args(num_expected_args):
    args = []
    for i in range(1, num_expected_args + 1):   # sys.argv[0] is script name
        try:
            args.append(sys.argv[i])
        except IndexError:  # put none in place of any arguments not found
            args.append(None)
    
    return args


if __name__ == '__main__':
    main()

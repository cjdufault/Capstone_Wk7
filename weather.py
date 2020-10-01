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
        ambiguous place names. It also allows for searching for places with
        the same name as a much better known place, such as Minneapolis, Kansas
        ('q=minneapolis,ks,us' works for this)."""
            
        # use metric by default, api uses kelvin by default
        if units == None:
            units = 'metric'
            
        parameters = {'q': location, 'units': units, 'appid': WEATHER_KEY}
        response = requests.get(API_URL, params=parameters).json()
        print(response)
                
    else:
        print('No API key found. Set it as an environment variable with the name, "WEATHER_KEY".')
        

# returns a list with a length equal to the number of expected arguments, with
# arguments that weren't entered represented as None
def get_args(num_expected_args):
    args = []
    for i in range(1, num_expected_args + 1):   # sys.argv[0] is the script name
        try:
            args.append(sys.argv[i])
        except IndexError:
            args.append(None)
    
    return args


if __name__ == '__main__':
    main()

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.urls import reverse
import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
import random
from urllib.request import urlopen
import json
import pyowm
import codecs
from .models import OptimalWeather
def canISwimToday(humid,windSpeed,location_current_weather_status,loc_pressure,location_clouds,location_rain,location_snow):
    return "yes"

def index(request):
    '''OptimalWeather.objects.create(min_temp=50,
    max_temp = 88,
    pressure =900,
    skycover = 100,
    water_avail = 1,
    humiditiy = 50,
    wind_speed = 180,
    wind_degree = 0,
    rain_forecast =  2)
    '''

    question=[2,3,4,5,6]
    print("llllll")
    owm = pyowm.OWM('4e1c1282f7896070089de33c4fc08a37')

    # Automatically geolocate the connecting IP
    f = urlopen('http://freegeoip.net/json/')
    json_string = (f.read())
    f.close()
    #location=json_string
    #location = json.loads(json_string)
    #reader = codecs.getreader("utf-8")
    #location=json_string.readall().decode('utf-8')
    #location = json.load(location)
    location=json.loads(json_string.decode("utf-8"))
    print(location)

    # Verifyng the current location of the device
    #print(location)
    # Output:
    # {u'city': u'Raleigh', u'region_code': u'NC', u'region_name': u'North Carolina', u'ip': u'152.7.224.5',
    # u'time_zone': u'America/New_York', u'longitude': -78.7239, u'metro_code': 560, u'latitude': 35.7463, u'country_code': u'US',
    # u'country_name': u'United States', u'zip_code': u'27606'}



    # Storing the details of the current location
    location_city = location['city']
    location_state = location['region_name']
    location_country = location['country_code']
    location_zip = location['zip_code']

    # Creating input string for the weather API
    current_location = location_city + "," + location_country

    # print current_location
    # Output:
    # Raleigh,United States


    observation = owm.weather_at_place(current_location)
    weather = observation.get_weather()
    location_pressure=weather.get_pressure()
    loc_pressure=location_pressure['press']
    location_wind = weather.get_wind()  # {u'speed': 2.46, u'deg': 82.5049}
    print("ssss")
    # Wind Speed and direction
    location_wind_speed = str(location_wind['speed']) + " mph"
    location_wind_direction = str(location_wind['deg']) + " degrees"
    location_clouds=weather.get_clouds()
    location_rain=weather.get_rain()
    location_snow=weather.get_snow()
    # Temperature in Fahrenheit : min, max and current
    location_temperature_farenheit = weather.get_temperature('fahrenheit')

    location_min_temp = location_temperature_farenheit['temp_min']
    location_max_temp = location_temperature_farenheit['temp_max']
    location_current_temp = location_temperature_farenheit['temp']

    # Curent detailed weather status
    location_current_weather_status = weather.get_detailed_status()
    #print(location_current_weather_status)


    # Current Humidity
    location_humidity_percentage = str(weather.get_humidity()) + "%"

    # Table for optimal swimming values
    optimal_swimming_temp_values = {'max_temp': 84, 'min_temp': 74}
    #answer=canISwimToday(weather.get_humidity(),location_wind['speed'],location_current_weather_status)

    # canISwimToday(optimal_swimming_temp_values,location_current_temp,location_current_weather_status)
    # canIHaveAPoolParty(forcasted_weather_conditions and calendar api intergration)
    # shouldPoolBeClosedToday(forecast weather condtions for the day)
    context = {
        #"qw_1": json.dumps(location_current_weather_status),
        "qw_1":json.dumps(weather.get_clouds()),
        "reply": canISwimToday(weather.get_humidity(),location_wind['speed'],location_current_weather_status,loc_pressure,location_clouds,location_rain,location_snow),
        # "qw_2":json.dumps(list(question_1)),
        # "qw_3":json.dumps(list(question_2)),
        # "qw_4":json.dumps(list(question_3)),
    }

    # def canISwimToday(self,optimal_swimming_temp_values,location_current_weather_status):

    #  Write function to compare current weather conditions with optimal weather conditions and
    # and then decide whether or not to give suggestion to swim.

    # .....
    return JsonResponse(context)





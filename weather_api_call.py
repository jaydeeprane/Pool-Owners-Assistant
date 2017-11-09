import urllib2
import json
import pyowm  

owm = pyowm.OWM('4e1c1282f7896070089de33c4fc08a37')

# Automatically geolocate the connecting IP
f = urllib2.urlopen('http://freegeoip.net/json/')
json_string = f.read()
f.close()
location = json.loads(json_string)

# Verifyng the current location of the device
# print(location)

# Output:
# {u'city': u'Raleigh', u'region_code': u'NC', u'region_name': u'North Carolina', u'ip': u'152.7.224.5', 
# u'time_zone': u'America/New_York', u'longitude': -78.7239, u'metro_code': 560, u'latitude': 35.7463, u'country_code': u'US', 
# u'country_name': u'United States', u'zip_code': u'27606'}



# Storing the details of the current location
location_city = location['city']
location_state = location['region_name']
location_country = location['country_name']
location_zip = location['zip_code']

# Creating input string for the weather API
current_location = location_city+","+location_country

# print current_location
# Output:
# Raleigh,United States


observation = owm.weather_at_place(current_location) 
weather = observation.get_weather() 

location_wind = weather.get_wind() #{u'speed': 2.46, u'deg': 82.5049}

# Wind Speed and direction
location_wind_speed = str(location_wind['speed'])+ " mph"
location_wind_direction = str(location_wind['deg']) + " degrees"

# Temperature in Fahrenheit : min, max and current
location_temperature_farenheit = weather.get_temperature('fahrenheit')

location_min_temp = location_temperature_farenheit['temp_min']
location_max_temp = location_temperature_farenheit['temp_max']
location_current_temp = location_temperature_farenheit['temp']

# Curent detailed weather status
location_current_weather_status = weather.get_detailed_status() 

# Current Humidity
location_humidity_percentage = str(weather.get_humidity())+"%"  


# Table for optimal swimming values
optimal_swimming_temp_values = {'max_temp':84,'min_temp':74}





# canISwimToday(optimal_swimming_temp_values,location_current_temp,location_current_weather_status)
# canIHaveAPoolParty(forcasted_weather_conditions and calendar api intergration)
# shouldPoolBeClosedToday(forecast weather condtions for the day)


# def canISwimToday(self,optimal_swimming_temp_values,location_current_weather_status):

#  Write function to compare current weather conditions with optimal weather conditions and
# and then decide whether or not to give suggestion to swim.

#.....

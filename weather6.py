import requests

url_current = 'http://api.openweathermap.org/data/2.5/onecall?lat=51.6711&lon=-1.2828&exclude=current,minutely,daily&appid=594987e67709714304cc3700fda762a2&units=metric'
request_current = requests.get(url_current)
data_current = request_current.json()

time_0 = data_current['hourly'][0]['dt']
temperature_0 = data_current['hourly'][0]['temp']
pressure_0 = data_current['hourly'][0]['pressure']
humidity_0 = data_current['hourly'][0]['humidity']
wind_speed_0 = data_current['hourly'][0]['wind_speed']
wind_direction_0 = data_current['hourly'][0]['wind_deg']

print('Time now: {}'.format(time_0))
print('Temperature now: {} °C'.format(temperature_0))
print('Air pressure now: {} Pa'.format(pressure_0))
print('Humidity now: {} %'.format(humidity_0))
print('Wind Speed now: {} m/s'.format(wind_speed_0))
print('Wind Direction now: {} °'.format(wind_direction_0))

url_historical = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt={}&appid=594987e67709714304cc3700fda762a2&units=metric'
url_historical = url_historical.replace('{}', str(time_0))

request_historical = requests.get(url_historical)
data_historical = request_historical.json()

time_historical = data_historical['hourly'][10]['dt']
temperature_historical = data_historical['hourly'][10]['temp']
pressure_historical = data_historical['hourly'][10]['pressure']
humidity_historical = data_historical['hourly'][10]['humidity']
wind_speed_historical = data_historical['hourly'][10]['wind_speed']
wind_direction_historical = data_historical['hourly'][10]['wind_deg']

print('Forecast Temperature: {} °C'.format(temperature_historical))
print('Forecast Air pressure: {} Pa'.format(pressure_historical))
print('Forecast Humidity: {} %'.format(humidity_historical))
print('Forecast Wind Speed: {} m/s'.format(wind_speed_historical))
print('Forecast Wind Direction: {} °'.format(wind_direction_historical))

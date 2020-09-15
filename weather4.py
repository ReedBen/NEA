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


url_historical = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt=1600092000&appid=594987e67709714304cc3700fda762a2&units=metric'
request_historical = requests.get(url_historical)
data_historical = request_historical.json()

time_14 = data_historical['hourly'][14]['dt']
temperature_14 = data_historical['hourly'][14]['temp']
pressure_14 = data_historical['hourly'][14]['pressure']
humidity_14 = data_historical['hourly'][14]['humidity']
wind_speed_14 = data_historical['hourly'][14]['wind_speed']
wind_direction_14 = data_historical['hourly'][14]['wind_deg']


print('Forecast Temperature: {} °C'.format(temperature_14))
print('Forecast Air pressure: {} Pa'.format(pressure_14))
print('Forecast Humidity: {} %'.format(humidity_14))
print('Forecast Wind Speed: {} m/s'.format(wind_speed_14))
print('Forecast Wind Direction: {} °'.format(wind_direction_14))

import requests

url = 'http://api.openweathermap.org/data/2.5/onecall?lat=51.6711&lon=-1.2828&exclude=current,minutely,daily&appid=594987e67709714304cc3700fda762a2&units=metric'
res = requests.get(url)
data = res.json()

temperature = data['hourly'][1]['temp']
pressure = data['hourly'][1]['pressure']
humidity = data['hourly'][1]['humidity']
wind_speed = data['hourly'][1]['wind_speed']
wind_direction = data['hourly'][1]['wind_deg']

print('Temperature : {} °C'.format(temperature))
print('Air pressure: {} Pa'.format(pressure))
print('Humidity: {} %'.format(humidity))
print('Wind Speed: {} m/s'.format(wind_speed))
print('Wind Direction: {} °'.format(wind_direction))

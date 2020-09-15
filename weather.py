import requests

url = 'http://api.openweathermap.org/data/2.5/weather?lat=51.6708&lon=-1.2880&appid=e80696a64fffd6b3a896d7ce2ced768f&units=metric'
res = requests.get(url)
data = res.json()

temperature = data['main']['temp']
pressure = data['main']['pressure']
humidity = data['main']['humidity']
wind_speed = data['wind']['speed']
wind_direction = data['wind']['deg']

print('Temperature : {} °C'.format(temperature))
print('Air pressure: {} Pa'.format(pressure))
print('Humidity: {} %'.format(humidity))
print('Wind Speed: {} m/s'.format(wind_speed))
print('Wind Direction: {} °'.format(wind_direction))

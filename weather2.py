import requests

url = 'http://pro.openweathermap.org/data/2.5/forecast/hourly?lat=51.6708&lon=-1.2880&appid=e80696a64fffd6b3a896d7ce2ced768f&units=metric'
res = requests.get(url)
data = res.json()

temperature = data['list']['1']['main']['temp']
pressure = data['list']['1']['main']['pressure']
humidity = data['list']['1']['main']['humidity']
wind_speed = data['list']['1']['wind']['speed']
wind_direction = data['list']['1']['wind']['deg']

print('Temperature : {} °C'.format(temperature))
print('Air pressure: {} Pa'.format(pressure))
print('Humidity: {} %'.format(humidity))
print('Wind Speed: {} m/s'.format(wind_speed))
print('Wind Direction: {} °'.format(wind_direction))



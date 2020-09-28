import requests
from datetime import datetime
import tkinter as tk
import csv
import matplotlib.pyplot as plt

url_current = 'http://api.openweathermap.org/data/2.5/onecall?lat=51.6711&lon=-1.2828&exclude=current,minutely,daily&appid=594987e67709714304cc3700fda762a2&units=metric'
request_current = requests.get(url_current)
data_current = request_current.json()

time_now = data_current['hourly'][0]['dt']
temperature_now = data_current['hourly'][0]['temp']
pressure_now = data_current['hourly'][0]['pressure']
humidity_now = data_current['hourly'][0]['humidity']
wind_speed_now = data_current['hourly'][0]['wind_speed']
wind_direction_now = data_current['hourly'][0]['wind_deg']
date = (datetime.utcfromtimestamp(time_now).strftime('%H:%M:%S %d-%m-%Y'))

print('Temperature now: {} °C'.format(temperature_now))
print('Air pressure now: {} Pa'.format(pressure_now))
print('Humidity now: {} %'.format(humidity_now))
print('Wind Speed now: {} m/s'.format(wind_speed_now))
print('Wind Direction now: {} °'.format(wind_direction_now))

url_forecast = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt={}&appid=594987e67709714304cc3700fda762a2&units=metric'
url_forecast = url_forecast.replace('{}', str(time_now))
request_forecast = requests.get(url_forecast)
data_forecast = request_forecast.json()

hour = -1
for hr in range(25):
    if data_forecast['hourly'][hr]['dt'] == time_now:
        hour = hr
    break

temperature_forecast = data_forecast['hourly'][hour]['temp']
pressure_forecast = data_forecast['hourly'][hour]['pressure']
humidity_forecast = data_forecast['hourly'][hour]['humidity']
wind_speed_forecast = data_forecast['hourly'][hour]['wind_speed']
wind_direction_forecast = data_forecast['hourly'][hour]['wind_deg']

print('Forecast Temperature: {} °C'.format(temperature_forecast))
print('Forecast Air pressure: {} Pa'.format(pressure_forecast))
print('Forecast Humidity: {} %'.format(humidity_forecast))
print('Forecast Wind Speed: {} m/s'.format(wind_speed_forecast))
print('Forecast Wind Direction: {} °'.format(wind_direction_forecast))

percentage_difference_temperature = round(((temperature_now - temperature_forecast) / temperature_now) * 100, 2)
percentage_difference_pressure = round(((pressure_now - pressure_forecast) / pressure_now) * 100, 2)
percentage_difference_humidity = round(((humidity_now - humidity_forecast) / humidity_now) * 100, 2)
percentage_difference_wind_speed = round(((wind_speed_now - wind_speed_forecast) / wind_speed_now) * 100, 2)
percentage_difference_wind_direction = round(abs((((wind_direction_now) - (wind_direction_forecast))) / wind_direction_now) * 100, 2)
if percentage_difference_wind_direction >= 180:
    percentage_difference_wind_direction -= 180
else:
    percentage_difference_wind_direction = percentage_difference_wind_direction

print('Percentage Difference for Temperature: {} %'.format(percentage_difference_temperature))
print('Percentage Difference for Pressure: {} %'.format(percentage_difference_pressure))
print('Percentage Difference for Humidity: {} %'.format(percentage_difference_humidity))
print('Percentage Difference for Wind Speed: {} %'.format(percentage_difference_wind_speed))
print('Percentage Difference for Wind Direction: {} %'.format(percentage_difference_wind_direction))

with open('weather.csv', mode='a') as weather_file:
    weather_file = csv.writer(weather_file, delimiter=',')
    weather_file.writerow([date, percentage_difference_temperature, percentage_difference_pressure, percentage_difference_humidity, percentage_difference_wind_speed, percentage_difference_wind_direction])

with open('weather_average.csv', mode='a') as weather_average_file:
    weather_average_file = csv.writer(weather_average_file, delimiter=',')
    weather_average_file.writerow([date, temperature_now, temperature_forecast, percentage_difference_temperature, pressure_now, pressure_forecast, percentage_difference_pressure, humidity_now, humidity_forecast, percentage_difference_humidity, wind_speed_now, wind_speed_forecast, percentage_difference_wind_speed, wind_direction_now, wind_direction_forecast, percentage_difference_wind_direction])

x = []
y = []
Percentage_Difference_name = ''

def get():
    number = type.get()
    with open('weather.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(str(row[0]))
            y.append(str(row[number]))
    if number == 1:
        Percentage_Difference_name = 'Temperature'
    elif number == 2:
        Percentage_Difference_name = 'Pressure'
    elif number == 3:
        Percentage_Difference_name = 'Humidity'
    elif number == 4:
        Percentage_Difference_name = 'Wind Speed'
    elif number == 5:
        Percentage_Difference_name = 'Wind Direction'
    plt.plot(x,y)
    plt.xlabel('Time')
    plt.ylabel('Percentage Difference (%)')
    plt.title('Percentage Difference in ' + Percentage_Difference_name +' over Time')
    plt.legend()
    plt.show()

root = tk.Tk()
type = tk.IntVar()

tk.Entry(textvariable=type).grid(column=0, row=0)
tk.Button(root, text="Enter then press: 1 for Temperature, 2 for Pressure, 3 for Humidity, 4 for Wind Speed, 5 Wind Direction", command=get).grid(column=1, row=0)

root.mainloop()

import weather
from datetime import datetime
import csv
import matplotlib.pyplot as plt

def accuracy(name, name_type):
    history = weather.history()
    forecasts = weather.forecasts()
    x = []
    y = []
    with open('weather.csv','w+') as weatherfile:
        weatherfile = csv.reader(weatherfile, delimiter=',')
    for dt in forecasts:
        if dt in history:
            date = (datetime.utcfromtimestamp(dt).strftime('%H:%M %d-%m'))
            percentage_difference = round(((history[dt][name] - forecasts[dt][0][name]) / history[dt][name]) * 100, 2)
            with open('weather.csv', mode='a', newline='') as weatherfile:
                weatherfile = csv.writer(weatherfile, delimiter=',')
                weatherfile.writerow([date, percentage_difference])
    with open('weather.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(str(row[0]))
            y.append(str(row[1]))
        plt.plot(x,y)
        plt.xticks(rotation = 45)
        plt.xlabel('Time')
        plt.ylabel('Percentage Difference (%)')
        plt.title('Percentage difference in ' + name_type + ' over time.')
        plt.show()

accuracy('temp', 'Temperature')

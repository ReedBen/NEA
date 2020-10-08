import weather
import http.server
import os
import urllib
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

def str_to_bytes(string):
    return string.encode('utf-8')

def nice_name(name):
    names = {'temp': 'Temperature',
        'pressure': 'Pressure',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'wind_deg': 'Wind Direction'}
    return names[name]

class Outputter(ABC):

    def Start(self):
        pass
    def Row(self):
        pass
    def End(self):
        pass

class TableOutputter(Outputter):
    def Start(self):
        pass
    def Row(self):
        pass
    def End(self):
        pass

class GraphOutputtter(Outputter):

    def Start(self):
        global weatherfile
        with open('weather.csv', mode='w', newline='') as weatherfile:
            weatherfile = csv.writer(weatherfile, delimiter=',')
    def Row(self):
        with open('weather.csv', mode='w', newline='') as weatherfile:
            weatherfile = csv.writer(weatherfile, delimiter=',')
        for forecast in forecasts:
            if forecast in history:
                date = (datetime.utcfromtimestamp(forecast).strftime('%H:%M %d-%m'))
                percentage_difference = (((history[forecast][name] - forecasts[forecast][0][name]) / history[forecast][name]) * 100)
                weatherfile.writerow([date, percentage_difference])
    def End(self):
        x = []
        y = []
        with open('weather.csv','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(str(row[0]))
                y.append(float(row[1]))
            fig = plt.figure(figsize=(20,10))
            plt.plot(x,y)
            plt.xticks(rotation = 45)
            plt.xlabel('Time')
            plt.ylabel('Percentage Difference (%)')
            plt.title('Percentage difference in ' + nice_name(name) + ' over time.')
            fig.savefig("weather")
            global line
            line = '<img src="/weather.png"><br>'

global G
G = GraphOutputtter()

class WeatherHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("In get" + self.path)
        if self.path.startswith('/cgi-bin/'):
            global name
            name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['id'][0]
            global history
            history = weather.history()
            global forecasts
            forecasts = weather.forecasts()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str_to_bytes('<!DOCTYPE html>'))
            self.wfile.write(str_to_bytes('<html><body>'))
            self.wfile.write(str_to_bytes('<a href="/form.html">Back</a><br>'))
            G.Start()
            G.Row()
            G.End()
            self.wfile.write(str_to_bytes(line))
            self.wfile.write(str_to_bytes('</body></html>'))
        else:
            path = self.path[1:]
            if os.path.exists(path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(path, 'rb') as contents:
                    self.wfile.write(contents.read())

server = http.server.HTTPServer(('', 8080), WeatherHandler)
server.serve_forever()








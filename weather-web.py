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

    def Rows(self):
        forecasts = weather.forecasts()
        history = weather.history()
        for forecast in forecasts:
            if forecast in history:
                date = (datetime.utcfromtimestamp(forecast).strftime('%H:%M %d-%m'))
                percentage_difference = (((history[forecast][self.name] - forecasts[forecast][0][self.name]) / history[forecast][self.name]) * 100)
                self.Row(date, percentage_difference)

    @abstractmethod
    def Row(self, date, percentage_difference):
        pass

    def End(self):
        pass

class TableOutputter(Outputter):
    def __init__(self, wfile, name):
        self.wfile = wfile
        self.name = name
    def Start(self):
        self.wfile.write(str_to_bytes('<style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body>'))
        self.wfile.write(str_to_bytes('<table style="width:100%"><tr><th>Date</th><th>'))
        line = nice_name(self.name)
        self.wfile.write(str_to_bytes(line))
        self.wfile.write(str_to_bytes('</th></tr>'))

    def Row(self, date, percentage_difference):
        line = '<tr><td>%s</td><td>%f</td></tr>' % (date, percentage_difference)
        self.wfile.write(str_to_bytes(line))

    def End(self):
        self.wfile.write(str_to_bytes('</table>'))

class GraphOutputtter(Outputter):
    def __init__(self, wfile, name):
        self.wfile = wfile
        self.name = name

    def Start(self):
        self.file = open('weather.csv', mode='w', newline='')
        self.weatherfile = csv.writer(self.file, delimiter=',')

    def Row(self, date, percentage_difference):
        self.weatherfile.writerow([date, percentage_difference])

    def End(self):
        x = []
        y = []
        self.file.close()
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
            plt.title('Percentage difference in ' + nice_name(self.name) + ' over time.')
            fig.savefig("weather")
            line = '<img src="/weather.png"><br>'
            self.wfile.write(str_to_bytes(line))


class WeatherHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("In get" + self.path)
        if self.path.startswith('/cgi-bin/'):
            try:
                name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['id'][0]
                form = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['type'][0]
            except:
                self.send_error(404)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str_to_bytes('<!DOCTYPE html>'))
            self.wfile.write(str_to_bytes('<html><body>'))
            self.wfile.write(str_to_bytes('<a href="/form.html">Back</a><br>'))
            try:
                nice_name(name)
                form_valid=True
                if form == 'Graph':
                    O = GraphOutputtter(self.wfile, name)
                elif form == 'Table':
                    O = TableOutputter(self.wfile, name)
                else:
                    form_valid = False

                if form_valid:
                    O.Start()
                    O.Rows()
                    O.End()
                else:
                    self.wfile.write(str_to_bytes('<p>Error</p><br>'))
            except:
                self.wfile.write(str_to_bytes('<p>Error</p><br>'))
            self.wfile.write(str_to_bytes('</body></html>'))
        else:
            path = self.path[1:]
            if os.path.exists(path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(path, 'rb') as contents:
                    self.wfile.write(contents.read())
            else:
                self.send_error(404)

server = http.server.HTTPServer(('', 8080), WeatherHandler)
server.serve_forever()

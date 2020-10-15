#This imports the weather module to use the relevant dictionairies
import weather
import http.server
import os
import urllib
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from abc import ABC, abstractmethod

# This function will be used to format the python input into a useable format for the html script
def str_to_bytes(string):
    return string.encode('utf-8')

#This dicitonairy is to take the requested measurement and output with a readable description
def nice_name(name):
    names = {'temp': 'Temperature (Celsius)',
        'pressure': 'Pressure (Pa)',
        'humidity': 'Humidity (%)',
        'wind_speed': 'Wind Speed (m/s)',
        'wind_deg': 'Wind Direction (Degrees)'}
    return names[name]

#This is a abstract class to establish the format for the other classes
class Outputter(ABC):

    def Start(self):
        pass

    #This function has some code in as it is used in both other classes
    #This takes the two dicitonaires and works out the percentage difference for same time in the two dictionaries
    #This does this for all the data in the forecast dictionairy and the corresponding times for the historical data
    #The percentage difference is the % of the actual data(histoical)-the predicted(forecast)
    def Rows(self):
        forecasts = weather.forecasts()
        history = weather.history()
        for forecast in forecasts:
            if forecast in history:
                date = (datetime.utcfromtimestamp(forecast).strftime('%H:%M %d-%m'))
                #For the percentage differnence in wind direction I needed an extra step due to it being calcualted in a part of 360 degrees where the actual percentage difference could be smaller than with the standard calulation
                #This is because the direction is in a circle, so a problem could be the differnece between the magnitudes 340 and 20. With the standard calculated the magnitude value would be 320 when the actual magnitde differnce is only 40
                #So to solve this problem, if the percentage value is over 180, -180. If the percentage value doesn't need to change
                if not self.name == 'wind_deg':
                    percentage_difference = (((history[forecast][self.name] - forecasts[forecast][0][self.name]) / history[forecast][self.name]) * 100)
                else:
                    percentage_difference = abs(forecasts[forecast][0][self.name] - history[forecast][self.name])
                    if percentage_difference > 180:
                        percentage_difference = 360 - percentage_difference
                history_data = history[forecast][self.name]
                forecast_data = forecasts[forecast][0][self.name]
                self.Row(date, percentage_difference, history_data, forecast_data)

    #@abstractmethod is used to make sure this function is used
    #Date and percentage difference variables and used in both classes so establsihed here
    @abstractmethod
    def Row(self, date, percentage_difference, history_data, forecast_data):
        pass

    def End(self):
        pass

#This class is for one of the output options
#The class inherits form the abstract class
class TableOutputter(Outputter):
    #This takes a copy of the variables so that they can be used in the functions
    def __init__(self, wfile, name):
        self.wfile = wfile
        self.name = name

    #This inputs the data
    #This writes some code to the html file so when the table is input it is in a format html understands
    #There is some code so the table outputted is more aesthetically pleasing
    #It also takes the inputted measurement's more readable name
    def Start(self):
        self.wfile.write(str_to_bytes('<style>table, th, td {border: 1px solid black;border-collapse: collapse;}th, td {padding: 15px;}</style></head><body>'))
        self.wfile.write(str_to_bytes('<table style="width:100%"><tr><th>Date</th><th>'))
        line = 'Percentage difference in ' + nice_name(self.name) + ' over time.'
        self.wfile.write(str_to_bytes(line))
        self.wfile.write(str_to_bytes('</th><th>Actual</th><th>Forecast</th></tr>'))

    #This processes the data
    #This writes the percentage difference to the table for each time
    def Row(self, date, percentage_difference, history_data, forecast_data):
        line = '<tr><td>%s</td><td>%f</td><td>%s</td><td>%f</td></tr>' % (date, percentage_difference, history_data, forecast_data)
        self.wfile.write(str_to_bytes(line))

    #This closes the table
    def End(self):
        self.wfile.write(str_to_bytes('</table>'))

#This class is for one of the output options
#The class inherits form the abstract class
class GraphOutputtter(Outputter):
    #This takes a copy of the variables so that they can be used in the functions
    def __init__(self, wfile, name):
        self.wfile = wfile
        self.name = name

    #This inputs the data
    #This opens the csv file and then creates a variable so that it can be used in other functions in the class
    def Start(self):
        self.file = open('weather.csv', mode='w', newline='')
        self.weatherfile = csv.writer(self.file, delimiter=',')

    #This processes the data
    #The function takes the function from the parent class
    #It then writes the percentage difference data to the comma seperated value file
    def Row(self, date, percentage_difference, history_data, forecast_data):
        self.weatherfile.writerow([date, percentage_difference, history_data, forecast_data])

    #This outputs the data
    #This code reads the data from the csv file
    #This is so that I can plot the data into a graph using MatPlotLib
    #It reads from the row with the time in and one of the rows with one of the calculations depending on which type was chosen
    #This code takes the users input and plots the type into a graph
    def End(self):
        self.file.close()
        with open('weather.csv','r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            x = []
            yplot = {'Percentage Difference': [], 'History': [], 'Forecast': []}
            for row in plots:
                x.append(str(row[0]))
                #This is to plot the three seperate y values on the same axes
                yplot['Percentage Difference'].append(float(row[1]))
                yplot['History'].append(float(row[2]))
                yplot['Forecast'].append(float(row[3]))
            fig = plt.figure(figsize=(13,6))
            ax = plt.axes()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(24))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
            plt.plot(x,yplot['Percentage Difference'], label='% Difference')
            plt.plot(x,yplot['History'], label='Actual')
            plt.plot(x,yplot['Forecast'], label='Forecast')
            plt.legend()
            plt.grid()
            plt.xlabel('Time')
            plt.ylabel('Percentage Difference (%)')
            raw_data = ax.secondary_yaxis('right')
            raw_data.set_ylabel('Raw data')
            plt.title('Percentage difference in ' + nice_name(self.name) + ' over time.')
            fig.savefig("weather")
            line = '<img src="/weather.png"><br>'
            self.wfile.write(str_to_bytes(line))

#This class is for the server side of the program
class WeatherHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("In get" + self.path)
        #This checks whether user has inputted something to the form
        if self.path.startswith('/cgi-bin/'):
            #This is some error handling to check that the name and form are useable
            #The varaible is created to input the requested types into the relevant output form for that measurement
            try:
                name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['id'][0]
                form = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['type'][0]
            except:
                self.send_error(404)
            #This code is so that html understands the output from python
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str_to_bytes('<!DOCTYPE html>'))
            self.wfile.write(str_to_bytes('<html><body>'))
            self.wfile.write(str_to_bytes('<a href="/form.html">Back</a><br>'))
            #This is some error handling to make sure that the url is in a correct state
            try:
                nice_name(name)
                form_valid=True
                #This takes the requested output from the user and takes the relevant class for the output
                if form == 'Graph':
                    O = GraphOutputtter(self.wfile, name)
                elif form == 'Table':
                    O = TableOutputter(self.wfile, name)
                else:
                    form_valid = False
                #This applies the class functions for the class requested by the user
                if form_valid:
                    O.Start()
                    O.Rows()
                    O.End()
                else:
                    #This is some error handling
                    self.wfile.write(str_to_bytes('<p>Error</p><br>'))
            except:
                #This is some error handling
                self.wfile.write(str_to_bytes('<p>Error</p><br>'))
            self.wfile.write(str_to_bytes('</body></html>'))
        else:
            #This is for when the user hans't inputted anything
            path = self.path[1:]
            if os.path.exists(path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open(path, 'rb') as contents:
                    self.wfile.write(contents.read())
            else:
                #This is some error handling
                self.send_error(404)

#This to locally run the server
server = http.server.HTTPServer(('', 8080), WeatherHandler)
server.serve_forever()

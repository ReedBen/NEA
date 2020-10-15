#This imports the weather module to use the relevant dictionairies
import weather
import http.server
import os
import urllib
from datetime import datetime
import csv
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

# This function will be used to format the python input into a useable format for the html script
def str_to_bytes(string):
    return string.encode('utf-8')

#This dicitonairy is to take the requested measurement and output with a readable description
def nice_name(name):
    names = {'temp': 'Temperature',
        'pressure': 'Pressure',
        'humidity': 'Humidity',
        'wind_speed': 'Wind Speed',
        'wind_deg': 'Wind Direction'}
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
                percentage_difference = (((history[forecast][self.name] - forecasts[forecast][0][self.name]) / history[forecast][self.name]) * 100)
                self.Row(date, percentage_difference)

    #@abstractmethod is used to make sure this function is used
    #Date and percentage difference variables and used in both classes so establsihed here
    @abstractmethod
    def Row(self, date, percentage_difference):
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
        line = nice_name(self.name)
        self.wfile.write(str_to_bytes(line))
        self.wfile.write(str_to_bytes('</th></tr>'))

    #This processes the data
    #This writes the percentage difference to the table for each time
    def Row(self, date, percentage_difference):
        line = '<tr><td>%s</td><td>%f</td></tr>' % (date, percentage_difference)
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
    def Row(self, date, percentage_difference):
        self.weatherfile.writerow([date, percentage_difference])

    #This outputs the data
    #This code reads the data from the csv file
    #This is so that I can plot the data into a graph using MatPlotLib
    #It reads from the row with the time in and one of the rows with one of the calculations depending on which type was chosen
    #This code takes the users input and plots the type into a graph
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

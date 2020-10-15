#This imports the weather module to use the relevant dictionairies
import weather
import http.server
import os
import urllib

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

#This class is for the server side of the program
class WeatherHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print("In get" + self.path)
        #This checks whether user has inputted something to the form
        if self.path.startswith('/cgi-bin/'):
            #This is some error handling to check that the name and form are useable
            #The varaible is created to input the requested types into the relevant output form for that measurement
            name = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['id'][0]
            #This code is so that html understands the output from python
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str_to_bytes('<!DOCTYPE html>'))
            self.wfile.write(str_to_bytes('<html><body>'))
            self.wfile.write(str_to_bytes('<a href="/form.html">Back</a><br>'))
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

#This to locally run the server
server = http.server.HTTPServer(('', 8080), WeatherHandler)
server.serve_forever()

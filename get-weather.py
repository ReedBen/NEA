import calendar
import requests
import time
#This imports the weatherconstansts module to use the relevant data
import weatherconstants

#This takes the current time
now = time.gmtime()
now_unix = calendar.timegm(now)

#This function is to write the data from the API to a text file
#This is so that it can be used in the relevant directory
def save_weather_data(url, file_path):
    with (open(file_path, "w")) as weather_file:
        weather_file.write(requests.get(url).text)

#This takes the API forecast data and reads the whole requests json and saves it into the text file for the current time
url_forecast = 'http://api.openweathermap.org/data/2.5/onecall?lat=51.6711&lon=-1.2828&exclude=current,minutely,daily&appid=594987e67709714304cc3700fda762a2&units=metric'
save_weather_data(url_forecast, '%s%d.txt' % (weatherconstants.get_forecast_dir(), now_unix))

#This takes the API history data and reads the whole requests json and saves it into the text file for the past five days from the current time
url_history = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt=%d&appid=594987e67709714304cc3700fda762a2&units=metric' % (now_unix)
save_weather_data(url_history, '%stoday%d.txt' % (weatherconstants.get_history_dir(), now_unix))

#This calculates one day from the current day to get yesterdays measurements
one_day = 24 * 60 * 60
yesterday_unix = now_unix - one_day

#This takes the API historical dfata and reads the whole requests json and saves it into the text file for the past five days from yesterday
url_history = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt=%d&appid=594987e67709714304cc3700fda762a2&units=metric' % (yesterday_unix)
save_weather_data(url_history, '%syesterday%d.txt' % (weatherconstants.get_history_dir(), now_unix))

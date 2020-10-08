import calendar
import requests
import time
import weatherconstants

now = time.gmtime()
now_unix = calendar.timegm(now)

def save_weather_data(url, file_path):
    with (open(file_path, "w")) as weather_file:
        weather_file.write(requests.get(url).text)

url_forecast = 'http://api.openweathermap.org/data/2.5/onecall?lat=51.6711&lon=-1.2828&exclude=current,minutely,daily&appid=594987e67709714304cc3700fda762a2&units=metric'
save_weather_data(url_forecast, '%s%d.txt' % (weatherconstants.get_forecast_dir(), now_unix))

url_history = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt=%d&appid=594987e67709714304cc3700fda762a2&units=metric' % (now_unix)
save_weather_data(url_history, '%stoday%d.txt' % (weatherconstants.get_history_dir(), now_unix))

one_day = 24 * 60 * 60
yesterday_unix = now_unix - one_day

url_history = 'http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=51.6711&lon=-1.2828&dt=%d&appid=594987e67709714304cc3700fda762a2&units=metric' % (yesterday_unix)
save_weather_data(url_history, '%syesterday%d.txt' % (weatherconstants.get_history_dir(), now_unix))


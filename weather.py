import json
import os
import weatherconstants

def history():
    weather_history = {}
    history_dir = weatherconstants.get_history_dir()

    for weather_file in os.listdir(history_dir):
        with open(history_dir+weather_file, 'r') as weather_file:
                txt = weather_file.read()
                js = json.loads(txt)
                for hour_data in js['hourly']:
                    if not hour_data['dt'] in weather_history:
                        weather_history[hour_data['dt']] = hour_data
    return weather_history

def forecasts():
    weather_forecasts = {}
    forecast_dir = weatherconstants.get_forecast_dir()

    for weather_file in os.listdir(forecast_dir):
        with open(forecast_dir+weather_file, 'r') as weather_file:
            txt = weather_file.read()
            js = json.loads(txt)
            first_dt = js['hourly'][0]['dt']
            if not first_dt in weather_forecasts:
                weather_forecasts[first_dt] = js['hourly']

    return weather_forecasts

if __name__ == '__main__':
    print(history())
    print(forecasts())


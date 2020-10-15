import json
import os
#This imports the weatherconstansts module to use the relevant data
import weatherconstants

#This function takes the historical data from the weatherconstants module
#The get-weather program runs every 15 minutes so there are 4 copies for each hour
#The function will only use the first mention of that hour so there aren't any repeats
#It takes the raw data from and sorts it using json so that the different measurements can be accessed
#It then adds it to the dictionairy
def history():
    weather_history = {}
    history_dir = weatherconstants.get_history_dir()

    for weather_file in os.listdir(history_dir):
        with open(history_dir+weather_file, 'r') as weather_file:
                txt = weather_file.read()
                js = json.loads(txt)
                #Error handling for if the data is missing or corupted
                try:
                    for hour_data in js['hourly']:
                        if not hour_data['dt'] in weather_history:
                            weather_history[hour_data['dt']] = hour_data
                except:
                    pass
    return weather_history

#This function takes the historical data from the weatherconstants module
#The get-weather program runs every 15 minutes so there are 4 copies for each hour
#The function will only use the first mention of that hour so there aren't any repeats
#It takes the raw data from and sorts it using json so that the different measurements can be accessed
#It then adds it to the dictionairy
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

#This allows the dictionairies used in other programs
if __name__ == '__main__':
    print(history())
    print(forecasts())

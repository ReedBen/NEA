import os

# Change this path to where the weather data is stored
# For simplicity you can use '/' as the path separator, even on Windows
# Make sure all paths end with a separator

#This tells the program where to find in the directory the data taken from the API
#The data is collected and then put in the folder by the get-weather program
def get_weather_dir():
   return handle_separator('C:/Users/Fido Squirtle/Desktop/data/')

#This is so that the path always ends with the correct separator
def handle_separator(path):
    if os.path.sep != '/':
        return path.replace('/', os.path.sep)
    return path

#This function takes the data from the data directory for the historical data from the API
def get_history_dir():
    return get_weather_dir() + handle_separator('history/')

#This function takes the data from the data directory for the forecast data from the API
def get_forecast_dir():
    return get_weather_dir() + handle_separator('forecast/')

#This allows the data from the historical and forecast to be used in other programs
if __name__ == '__main__':
    print('history dir is : %s' % get_history_dir())
    print('forecast dir is : %s' % get_forecast_dir())

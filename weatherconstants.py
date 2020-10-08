import os

# Change this path to where the weather data is stored
# For simplicity you can use '/' as the path separator, even on Windows
# Make sure all paths end with a separator

def get_weather_dir():
   return handle_separator('C:/Users/Fido Squirtle/Desktop/data/')

def handle_separator(path):
    if os.path.sep != '/':
        return path.replace('/', os.path.sep)
    return path

def get_history_dir():
    return get_weather_dir() + handle_separator('history/')

def get_forecast_dir():
    return get_weather_dir() + handle_separator('forecast/')

if __name__ == '__main__':
    print('history dir is : %s' % get_history_dir())
    print('forecast dir is : %s' % get_forecast_dir())

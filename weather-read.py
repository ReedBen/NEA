import weather
history = weather.history()
forecasts = weather.forecasts()

for forecast_time in forecasts:
    if forecast_time in history:
        print('%f - %f' % (history[forecast_time]['temp'], forecasts[forecast_time][0]['temp']))

import csv
import matplotlib.pyplot as plt

x = []
y = []
Percentage_Difference_name = ''
i = int(input('Enter 1 for Temperature, 2 for Pressure, 3 for Humidity, 4 for Wind Speed, 5 Wind Direction : '))

with open('weather.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(str(row[0]))
        y.append(str(row[i]))
if i == 1:
    Percentage_Difference_name = 'Temperature'
elif i == 2:
    Percentage_Difference_name = 'Pressure'
elif i == 3:
    Percentage_Difference_name = 'Humidity'
elif i == 4:
    Percentage_Difference_name = 'Wind Speed'
elif i == 5:
    Percentage_Difference_name = 'Wind Direction'
plt.plot(x,y)
plt.xlabel('Time')
plt.ylabel('Percentage Difference')
plt.title('Percentage Difference in ' + Percentage_Difference_name +' over Time')
plt.legend()
plt.show()

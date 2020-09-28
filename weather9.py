import tkinter as tk
import csv
import matplotlib.pyplot as plt
x = []
y = []
Percentage_Difference_name = ''

def get():
    number = type.get()
    with open('weather.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(str(row[0]))
            y.append(str(row[number]))
    if number == 1:
        Percentage_Difference_name = 'Temperature'
    elif number == 2:
        Percentage_Difference_name = 'Pressure'
    elif number == 3:
        Percentage_Difference_name = 'Humidity'
    elif number == 4:
        Percentage_Difference_name = 'Wind Speed'
    elif number == 5:
        Percentage_Difference_name = 'Wind Direction'
    plt.plot(x,y)
    plt.xlabel('Time')
    plt.ylabel('Percentage Difference (%)')
    plt.title('Percentage Difference in ' + Percentage_Difference_name +' over Time')
    plt.legend()
    plt.show()

root = tk.Tk()
type = tk.IntVar()

tk.Entry(textvariable=type).grid(column=0, row=0)
tk.Button(root, text="Enter then press: 1 for Temperature, 2 for Pressure, 3 for Humidity, 4 for Wind Speed, 5 Wind Direction", command=get).grid(column=1, row=0)

root.mainloop()

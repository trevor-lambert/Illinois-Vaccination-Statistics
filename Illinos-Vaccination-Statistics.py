from requests_html import HTMLSession
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk


# Web scraping
session = HTMLSession()
r = session.get('https://coronavirus.illinois.gov/s/vaccination-location')
r.html.render()
table_rows = r.html.find('tr')


# Find and sort data from web
data = []
locations = []
for row in table_rows:
    for entry in row.find('lightning-base-formatted-text'):
        if len(locations) < 6:
            locations.append(entry.text)
        else:
            data.append(locations.copy())
            locations.clear()
            locations.append(entry.text)
data.append(locations.copy())


# Dataframe
headers = ['Site Name', 'Location Type', 'Address', 'City', 'Zip', 'County']
dataframe = pd.DataFrame(data, columns=headers)
dataframe['County'] = dataframe['County'].str.upper()


# Bar Graph
dups_county = dataframe.pivot_table(index=['County'], aggfunc='size')
dups_county.plot(kind='barh', figsize=(20, 20))
plt.title('COVID-19 Vaccination Locations By Illinois County', fontsize=35)
plt.ylabel('County', fontsize=20)
plt.xlabel('# of Locations', fontsize=20)
plt.gca().invert_yaxis()
plt.xticks(np.arange(0, dups_county.max(), 5), fontsize=13)
plt.yticks(fontsize=13)
for index, value in enumerate(dups_county):
    plt.text(value, index, str(value))


# Dataframe/Values for GUI
NumLocationsDF = dataframe.count()
NumLocations = str(NumLocationsDF.iloc[0])
NumCounties = str(dataframe['County'].nunique())


# GUI
class CovidStats_GUI:
    def __init__(self):
        self.mainWindow = Tk()
        self.mainWindow.title('Current COVID-19 Illinois Vaccination Location Statistics')
        self.mainWindow.geometry('470x160')

        self.titleLabel = ttk.Label(self.mainWindow, text='COVID-19 Illinois Vaccination Location Statistics',\
                                    font=('Arial Bold', 20), borderwidth=2, relief='ridge')
        self.titleLabel.grid(row=0, column=0)

        self.Div = Label(self.mainWindow, text='')
        self.Div.grid(row=1, column=0)

        self.LocationNumLabel = Label(self.mainWindow, text='Current # of Locations: ' + NumLocations, font='Arial')
        self.LocationNumLabel.grid(row=3, column=0)

        self.CountyNumLabel = Label(self.mainWindow, text='Current # of Counties With Vaccination Location: '\
                                                          + NumCounties + '/102', font='Arial')
        self.CountyNumLabel.grid(row=4, column=0)

        self.plotButton = Button(self.mainWindow, text='Plot Distribution', command=self.plotButton_Click, font='Arial')
        self.plotButton.grid(row=2, column=0)

        self.exitButton = Button(self.mainWindow, text='Exit', command=self.mainWindow.destroy, font='Arial')
        self.exitButton.grid(row=5, column=0)

        self.mainWindow.mainloop()

    def plotButton_Click(self):
        plt.show()


def main():
    CovidStats_GUI()


main()

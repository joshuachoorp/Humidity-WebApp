"""
Filter and Clean data
"""

# Plot Weather data

import os
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as datetime
import numpy as np


# Function to read csv file
def readFile(file = (os.getcwd() + "/Datasets/compiledRegionData.csv")):
#def readFile(file = ("compiledRegionData.csv")):
    # Read csv file into Pandas Dataframe
    # dayfirst= True, parse_dates= True,   index_col=0,
    df = pd.read_csv(file, encoding="unicode-escape", usecols=[0,1,2,3,4,5,6,7])
    #df = pd.read_csv("Datasets/compiledRegionData.csv", encoding="unicode-escape", usecols=[0,1,2,3,4,5,6,7])
    #df = df.reset_index(inplace = True)
    #df = df.set_index('Date')
    pd.set_option('display.max_columns', None)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    return df

df = readFile()

# Function to filter through data and return a dictionary 
def dataforGraph(region, month, year, index):
    df = readFile()
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    dataforGraph_df = dataFilter_df[ [index] ].to_dict()
    #dataforGraph_Dict = convertToDict(dataforGraph_df)
    return (dataforGraph_df[index].values())


# Function to fetch data required for plotting all graphs
def dataPlot(region):
    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()
    print(uniqueYear[0])
    
    label = []
    valuesHumi = []
    valuesTemp = []

    # For loop to go through each year
    for i in range(len(uniqueYear)):
        # For loop to go through each month and get values for each specific month
        for j in range(len(uniqueMonth)):
            # Try and except to catch any errors on no matches for months and years
            try:
                label_df = df.loc[(df['Date'].dt.month == int(uniqueMonth[j]))]
                labelDates = label_df['Date'].dt.strftime("%d").unique().tolist()
                label.append(labelDates)
                valuesHumi.append(list(dataforGraph(region, int(uniqueMonth[j]), int(uniqueYear[i]), "Humidity_Avg")))
                valuesTemp.append(list(dataforGraph(region, int(uniqueMonth[j]), int(uniqueYear[i]), "Mean Temperature (Â°C)")))
            except Exception as e:
                print(e)
                pass
    

    dataPlot = [label, valuesHumi, valuesTemp]

    return dataPlot


# Function to create canvas names based on each unique month and year 
def canvasName(region):
    uniqueMonth = df['Date'].dt.strftime("%m-%y").unique().tolist()
    for i in range(len(uniqueMonth)):
        uniqueMonth[i] = "chart_" + region + "_" + uniqueMonth[i]
    return uniqueMonth


# filter weather data by month and region
def dataFilter(region, month, year):
    df = readFile()
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    return dataFilter_df 


# create variables to store the dictionary, which contains the mean value of all weather data from June to Aug by region
def calMeanWeatherData(data):
    meanWeatherData = calAvg(data)
    return meanWeatherData


# Function to get Highest, Mean and Lowest data for each month
def dataGroup(region):
    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()

    labelDisplay = []
    valuesDisplay = []

    # For loop to go through each year
    for i in range(len(uniqueYear)):
        # For loop to go through each month and get values for each specific month
        for j in range(len(uniqueMonth)):
            # Try and except to catch any errors on no matches for months and years
            try:
                print(uniqueMonth[i])
                labelDisplay.append(list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[j]), int(uniqueYear[i]))).keys()))
                valuesDisplay.append(list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[j]), int(uniqueYear[i]))).values()))
            except Exception as e:
                print(e)
                pass

    dataDisplay = [labelDisplay, valuesDisplay]

    return dataDisplay





north_june_df = df.loc[(df['Region'] == 'North') & (df['Date'].dt.month == 6) & (df['Date'].dt.year == 2023)] 
north_july_df = df.loc[(df['Region'] == 'North') & (df['Date'].dt.month == 7) & (df['Date'].dt.year == 2023)]
north_aug_df =  df.loc[(df['Region'] == 'North') & (df['Date'].dt.month == 8) & (df['Date'].dt.year == 2023)]

south_june_df = df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 6) & (df['Date'].dt.year == 2023)]
south_july_df = df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 7) & (df['Date'].dt.year == 2023)]
south_aug_df =  df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 8) & (df['Date'].dt.year == 2023)]

central_june_df = df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 6) & (df['Date'].dt.year == 2023)]
central_july_df = df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 7) & (df['Date'].dt.year == 2023)]
central_aug_df =  df.loc[(df['Region'] == 'South') & (df['Date'].dt.month == 8) & (df['Date'].dt.year == 2023)]

east_june_df = df.loc[(df['Region'] == 'East') & (df['Date'].dt.month == 6) & (df['Date'].dt.year == 2023)]
east_july_df = df.loc[(df['Region'] == 'East') & (df['Date'].dt.month == 7) & (df['Date'].dt.year == 2023)]
east_aug_df =  df.loc[(df['Region'] == 'East') & (df['Date'].dt.month == 8) & (df['Date'].dt.year == 2023)]

west_june_df = df.loc[(df['Region'] == 'West') & (df['Date'].dt.month == 6) & (df['Date'].dt.year == 2023)]
west_july_df = df.loc[(df['Region'] == 'West') & (df['Date'].dt.month == 7) & (df['Date'].dt.year == 2023)]
west_aug_df =  df.loc[(df['Region'] == 'West') & (df['Date'].dt.month == 8) & (df['Date'].dt.year == 2023)]

#print (north_june_df)

# Create function to filter the above Df and return Date, Humiditiy_Avg and Mean Temperature, which will be used for displaying on graph
# This functions comes before the calculation of weather data?
# take in arg: a df 



'''Display a graph showing Humidity_Avg and Mean Temperature in 1 month (June) for 1 region (North)'''
#filtered_north_june_df = dataforGraph(north_june_df)
#print (filtered_north_june_df)

#Plotting graph w 2 Y axes. first y-axes: Mean Temperature, second y-axes:: Humidity_Avg
#fig, ax1 = plt.subplots()
#ax1.plot(filtered_north_june_df['Date'], filtered_north_june_df['Mean Temperature (Â°C)'], color = "blue")
#ax1.set_xlabel('Dates in June', fontsize=14)
#ax1.set_ylabel("Mean Temperature (Â°C)", fontsize=14)
#ax1.set_title('Mean Temperature vs Humidity_Avg in North Region during June', fontsize=16)

#ax2 = ax1.twinx()
#ax2.plot (filtered_north_june_df['Date'], filtered_north_june_df["Humidity_Avg"], color = "orange")
#ax2.set_ylabel("Humidity_Avg", fontsize=14)
#plt.show()


def plotGraph(df):
    figure, ax1 = plt.subplots()
    ax1.plot(df['Date'], df['Mean Temperature (Â°C)'], color = "blue")
    ax1.set_xlabel('Dates', fontsize=14)
    ax1.set_ylabel("Mean Temperature (Â°C)", fontsize=14)
    ax1.set_title('Mean Temperature vs Humidity_Avg in North Region during July', fontsize=16)

    ax2 = ax1.twinx()
    ax2.plot (df['Date'], df["Humidity_Avg"], color = "orange")
    ax2.set_ylabel("Humidity_Avg", fontsize=14)
    plt

filtered_north_july_df = north_july_df
plotGraph(filtered_north_july_df)

# Create a function to collate the mean/average of the following weather data for 1 month 
# (Humidity_high, Humidity_avg, Humidity_low, Mean Temp, Max Temp, Lowest Temp)

def calAvg (filteredDf):

    avg_Hmd_h = 0
    avg_Hmd_a = 0
    avg_Hmd_l = 0

    avg_MeanTemp = 0
    avg_MaxTemp = 0
    avg_LowTemp = 0
    data = {}
    # Columns that need to get the mean, Humidity_h, Humidity_a, humidity_l, MeanTemp, MaxTemp, LowTemp
    # iterate through each column in the filtered df
    # if x == column name, proceed to calculate mean
    for x in filteredDf:
        if (x == "Humidity_High"):
            avg_Hmd_h = filteredDf[x].mean()
        elif (x == "Humidity_Avg"):
            avg_Hmd_a = filteredDf[x].mean()
        elif (x == 'Humidity_Low'):
            avg_Hmd_l = filteredDf[x].mean()
        elif (x == 'Mean Temperature (Â°C)'):
            avg_MeanTemp = filteredDf[x].mean()
        elif (x == 'Maximum Temperature (Â°C)'):
            avg_MaxTemp = filteredDf[x].mean()
        elif (x == "Lowest Temperature (Â°C)"):
            avg_LowTemp = filteredDf[x].mean()

    # Convert results and store it into Dictionary  
    data = {
        'Humidity_High': avg_Hmd_h,
        'Humidity_Avg': avg_Hmd_a,
        'Humidity_Low': avg_Hmd_l,
        'Mean Temperature (Â°C)': avg_MeanTemp,
        'Maximum Temperature (Â°C)': avg_MaxTemp,
        'Lowest Temperature (Â°C)': avg_LowTemp
    }
    #df = pd.DataFrame(data)
    #return df
    return data
    #return avg_Hmd_h, avg_Hmd_a, avg_Hmd_l, avg_MeanTemp, avg_MaxTemp, avg_LowTemp   # Results are returned in tuple form





north_june_mean_weather_data = calAvg(north_june_df) 
north_july_mean_weather_data = calAvg(north_july_df)
north_aug_mean_weather_data = calAvg(north_aug_df)

south_june_mean_weather_data = calAvg(south_june_df) 
south_july_mean_weather_data = calAvg(south_july_df)
south_aug_mean_weather_data = calAvg(south_aug_df)

central_june_mean_weather_data = calAvg(central_june_df) 
central_july_mean_weather_data = calAvg(central_july_df)
central_aug_mean_weather_data = calAvg(central_aug_df)

east_june_mean_weather_data = calAvg(east_june_df) 
east_july_mean_weather_data = calAvg(east_july_df)
east_aug_mean_weather_data = calAvg(east_aug_df)

west_june_mean_weather_data = calAvg(west_june_df) 
west_july_mean_weather_data = calAvg(west_july_df)
west_aug_mean_weather_data = calAvg(west_aug_df)


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
#def readFile(file = (os.getcwd() + "/Datasets/compiledRegionData.csv")):
def readFile(file = ("compiledRegionData.csv")):
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
                #print(e)
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
                labelDisplay.append(list(calMeanWeatherData(dataFilter(region, int(uniqueMonth[j]), int(uniqueYear[i]))).keys()))
                valuesDisplay.append(list(calMeanWeatherData(dataFilter(region, int(uniqueMonth[j]), int(uniqueYear[i]))).values()))
            except Exception as e:
                #print(e)
                pass

    dataDisplay = [labelDisplay, valuesDisplay]

    return dataDisplay


def canvasItems(region):
    uniqueMonth = df['Date'].dt.strftime("%m-%y").unique().tolist()
    items = []
    for j in range(len(uniqueMonth)):
        canvasItems = []
        canvasNameAppend = "chart_" + region + "_" + uniqueMonth[j]
        canvasItems.append(canvasNameAppend)
        items.append(canvasItems)
        
    return items



def dataCreateDiv(region):
    cItem = canvasItems(region)
    dataPlotItem = dataPlot(region)
    dataGroupItem = dataGroup(region)
    div = []
    for i in range(len(cItem)):
        divElements = []
        divElements.append(cItem[i])
        divElements.append(dataPlotItem[0][i])
        divElements.append(dataPlotItem[1][i])
        divElements.append(dataPlotItem[2][i])
        divElements.append(dataGroupItem[0][i])
        divElements.append(dataGroupItem[1][i])
        div.append(divElements)

    return div

#data = dataCreateDiv("North")
#print(data[0])




















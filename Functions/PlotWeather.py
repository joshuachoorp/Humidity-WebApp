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
def readFile(file = (os.getcwd() + "/Datasets/combinedRegionData.csv")):
#def readFile(file = "Datasets/combinedRegionData.csv"):

    # Read csv file into Pandas Dataframe
    df = pd.read_csv(file, encoding="unicode-escape", usecols=[0,1,2,3,4,5,6,7])
    pd.set_option('display.max_columns', None)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    return df

# Read csv file
df = readFile()

# Function to filter through data and return in the form of a dictionary 
def dataforGraph(region, month, year, index):
    df = readFile()
    # Filter data according to what is required
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    dataforGraph_df = dataFilter_df[ [index] ].to_dict()
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
                label_df = df.loc[(df['Date'].dt.month == int(uniqueMonth[j])) & (df['Region'] == region)]
                labelDates = label_df['Date'].dt.strftime("%d").unique().tolist()
                labelDates.sort()
                label.append(labelDates)
                valuesHumi.append(list(dataforGraph(region, int(uniqueMonth[j]), int(uniqueYear[i]), "Humidity_Avg")))
                valuesTemp.append(list(dataforGraph(region, int(uniqueMonth[j]), int(uniqueYear[i]), "Mean Temperature (°C)")))

            except Exception as e:
                #print(e)
                pass
    
    # Storing list of datas in a overall list
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
def calAvg(filteredDf):

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

        # Ensure that all data in the dataframe are type numbers and not string
        filteredDf[x] = pd.to_numeric(filteredDf[x], errors='coerce')

        if (x == "Humidity_High"):
            avg_Hmd_h = filteredDf[x].mean()
        elif (x == "Humidity_Avg"):
            avg_Hmd_a = filteredDf[x].mean()
        elif (x == 'Humidity_Low'):
            avg_Hmd_l = filteredDf[x].mean()
        elif (x == 'Mean Temperature (°C)'):
            avg_MeanTemp = filteredDf[x].mean()
        elif (x == 'Maximum Temperature (°C)'):
            avg_MaxTemp = filteredDf[x].mean()
        elif (x == "Lowest Temperature (°C)"):
            avg_LowTemp = filteredDf[x].mean()

    # Convert results and store it into Dictionary  
    data = {
        'Average Humidity_High': avg_Hmd_h,
        'Average Humidity_Avg': avg_Hmd_a,
        'Average Humidity_Low': avg_Hmd_l,
        'Average Mean Temperature (°C)': avg_MeanTemp,
        'Average Maximum Temperature (°C)': avg_MaxTemp,
        'Average Lowest Temperature (°C)': avg_LowTemp
    }

    return data   


# Function to get Average of the Highest, Mean and Lowest data for each month
def dataGroup(region):
    # Look for unique months in dataset and store in a list
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset and store in a list
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()

    labelDisplay = []
    valuesDisplay = []
    monthDisplay = []
    # For loop to go through each year
    for i in range(len(uniqueYear)):
        # For loop to go through each month and get values for each specific month
        for j in range(len(uniqueMonth)):
            # Try and except to catch any errors on no matches for months and years
            try:
                monthDisplay.append(uniqueMonth[j])
                labelDisplay.append(list(calAvg(dataFilter(region, int(uniqueMonth[j]), int(uniqueYear[i]))).keys()))
                valuesDisplay.append(list(calAvg(dataFilter(region, int(uniqueMonth[j]), int(uniqueYear[i]))).values()))
                
            except Exception as e:
                print(e)
                pass

    dataDisplay = [monthDisplay, labelDisplay, valuesDisplay]

    return dataDisplay

# Function to store items required to create canvas on html page
def canvasItems(region):
    uniqueMonth = df['Date'].dt.strftime("%m-%y").unique().tolist()
    items = []
    for j in range(len(uniqueMonth)):
        canvasItems = []
        canvasNameAppend = "chart_" + region + "_" + uniqueMonth[j]
        canvasItems.append(canvasNameAppend)
        items.append(canvasItems)
        
    return items


# Collate all data into overall list
# Each element in the list contains all required data to plot a graph and show relevant on html
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
        divElements.append(dataGroupItem[2][i])
        div.append(divElements)

    return div



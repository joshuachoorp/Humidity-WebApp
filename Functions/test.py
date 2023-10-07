import os
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as datetime
import numpy as np


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
def canvasName(region):
    uniqueMonth = df['Date'].dt.strftime("%m-%y").unique().tolist()
    for i in range(len(uniqueMonth)):
        uniqueMonth[i] = "chart_" + region + "_" + uniqueMonth[i]
    return uniqueMonth

uniqueDate = df['Date'].dt.strftime("%d-%m").unique().tolist()
#print(canvasName("North"))



def dataforGraph(region, month, year, index):
    df = readFile()
    
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    df['Date'] = df['Date'].dt.strftime('%d')
    dataforGraph_df = dataFilter_df[ [index] ].to_dict()
    #dataforGraph_Dict = convertToDict(dataforGraph_df)
    return (dataforGraph_df[index].values())

def dataPlot(region):
    # Look for unique months in dataset
    unique = df['Date'].dt.strftime("%m%y").unique().tolist()

    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()
    print(uniqueYear[0])
    
    label = []
    valuesHumi = []
    valuesTemp = []

    # For loop to go through each month and get values for each specific month
    for i in range(len(unique)):
        label_df = df.loc[(df['Date'].dt.month == int(uniqueMonth[i]))]
        labelDates = label_df['Date'].dt.strftime("%d").unique().tolist()
        label.append(labelDates)
        valuesHumi.append(list(dataforGraph(region, int(uniqueMonth[i]), int(uniqueYear[0]), "Humidity_Avg")))
        valuesTemp.append(list(dataforGraph(region, int(uniqueMonth[i]), int(uniqueYear[0]), "Mean Temperature (Â°C)")))

    dataPlot = [label, valuesHumi, valuesTemp]

    return dataPlot



#print(dataPlot("North"))
test1 = df.loc[(df['Date'].dt.month == 7)]
test = test1['Date'].dt.strftime("%d").unique().tolist()
#print(test)

label = []
uniqueDate1 = df['Date'].dt.strftime("%m%y").unique().tolist()
for i in range(len(uniqueDate1)):
    test1 = df.loc[(df['Date'].dt.month == int(uniqueDate1[i]))]
    test = test1['Date'].dt.strftime("%d").unique().tolist()
    #print(test)
    label.append(test)

uniqueYear = df['Date'].dt.strftime("%m").unique().tolist()
#print(uniqueYear)

#print(dataPlot("North", 2023))













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

# filter weather data by month and region
def dataFilter(region, month, year):
    df = readFile()
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    return dataFilter_df 


# create variables to store the dictionary, which contains the mean value of all weather data from June to Aug by region
def calMeanWeatherData(data):
    meanWeatherData = calAvg(data)
    return meanWeatherData


def dataGroup1(region):

    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()
    print(uniqueMonth)

    labelDisplay = []
    valuesDisplay = []

    for i in range(len(uniqueMonth)):
        print(uniqueMonth[i])
        labelDisplay.append(list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[i]), int(uniqueYear[0]))).keys()))
        valuesDisplay.append(list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[i]), int(uniqueYear[0]))).values()))

    dataDisplay = [labelDisplay, valuesDisplay]

    return dataDisplay



def dataGroup(region, year=2023):
    # Look for unique months in dataset
    unique = df['Date'].dt.strftime("%m%y").unique().tolist()

    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.month.unique()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.is_leap_year.unique()

    labelDisplay = []
    valuesDisplay = []
    
    label = [list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[0]), int(uniqueYear[0]))).keys()),
                  list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[1]), int(uniqueYear[0]))).keys()),
                  list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[2]), int(uniqueYear[0]))).keys())]
    
    valuesNorth = [list(calMeanWeatherData(dataFilter(region.capitalize(), int(uniqueMonth[0]), int(uniqueYear[0]))).values()),
                   list(calMeanWeatherData(dataFilter(region.capitalize(), 7, year)).values()),
                   list(calMeanWeatherData(dataFilter(region.capitalize(), 8, year)).values())]

    dataDisplay = [label, valuesNorth]

    return dataDisplay


uniqueYear1 = df['Date'].dt.year.unique()
print(type(uniqueYear1[0]))
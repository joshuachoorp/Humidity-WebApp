import os
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as datetime
import numpy as np


# Function to read csv file
#def readFile(file = (os.getcwd() + "/Datasets/compiledRegionData.csv")):
def readFile(file = ("Functions/compiledRegionData.csv")):
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
def dataPlot():
    # Look for unique months in dataset
    uniqueMonth = df['Date'].dt.strftime("%m").unique().tolist()

    # Look for unique months in dataset
    uniqueYear = df['Date'].dt.strftime("%Y").unique().tolist()
    print(uniqueYear[0])

    uniqueRegion = df['Region'].unique().tolist()
    
    items = []
    elementsAccess = []
    label = []
    valuesHumi = []
    valuesTemp = []
    for k in range(len(uniqueRegion)):
        # For loop to go through each year
        for i in range(len(uniqueYear)):
            # For loop to go through each month and get values for each specific month
            for j in range(len(uniqueMonth)):
                # Try and except to catch any errors on no matches for months and years
                try:
                    label_df = df.loc[(df['Date'].dt.month == int(uniqueMonth[j]))]
                    labelDates = label_df['Date'].dt.strftime("%d").unique().tolist()
                    label.append(labelDates)
                    valuesHumi.append(list(dataforGraph(uniqueRegion[k], int(uniqueMonth[j]), int(uniqueYear[i]), "Humidity_Avg")))
                    valuesTemp.append(list(dataforGraph(uniqueRegion[k], int(uniqueMonth[j]), int(uniqueYear[i]), "Mean Temperature (Â°C)")))

                    elementsAccess.append(uniqueRegion[k])
                    elementsAccess.append()

                except Exception as e:
                    print(e)
                    pass
    

    dataPlot = [label, valuesHumi, valuesTemp]

    return dataPlot

#print(canvasName())

uniqueMonthYear = df['Date'].dt.strftime("%m-%Y").unique().tolist()
uniqueRegion = df['Region'].unique().tolist()

items = []

for i in range(len(uniqueMonthYear)):
    elementsAccess = []
    elementsAccess.append(uniqueMonthYear[i])
    elementsAccess.append(uniqueRegion[i])
    items.append(elementsAccess)

#print(items)

#print(uniqueRegion)
#print(dataPlot("uniqueRegion"))



def canvasItems():
    uniqueRegion = df['Region'].unique().tolist()
    uniqueMonth = df['Date'].dt.strftime("%m-%y").unique().tolist()
    items = []
    for j in range(len(uniqueMonth)):
        for i in range(len(uniqueRegion)):
            canvasItems = []
            canvasNameAppend = "chart_" + uniqueRegion[i] + "_" + uniqueMonth[j]
            canvasItems.append(canvasNameAppend)
            items.append(canvasItems)
            
    return items


def dataPlotTest(region):
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



def dataCreateDiv():
    cItem = canvasItems()
    dataPlotItem = dataPlot()
    testItems = []
    for i in range(len(cItem)):
        test = []
        test.append(cItem[i])
        test.append(dataPlotItem[0][i])
        test.append(dataPlotItem[1][i])
        test.append(dataPlotItem[2][i])
        testItems.append(test)
    return testItems

print(len(dataCreateDiv()))



array = []
array1 = [1, 2, 3]




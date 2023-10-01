# Plot Weather data

import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as datetime
import numpy as np


def readFile():
    # Read csv file into Pandas Dataframe
    # dayfirst= True, parse_dates= True,   index_col=0,
    df = pd.read_csv("Datasets/compiledRegionData.csv", encoding="unicode-escape", usecols=[0,1,2,3,4,5,6,7])
    #df = df.reset_index(inplace = True)
    #df = df.set_index('Date')
    pd.set_option('display.max_columns', None)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    return df

df = readFile()

# filter weather data by month and region
def dataFilter(region, month, year):
    df = readFile()
    dataFilter_df = df.loc[(df['Region'] == region.capitalize()) & (df['Date'].dt.month == month) & (df['Date'].dt.year == year)]
    return dataFilter_df 

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

#print(type(june_mean_weather_data))
#print (north_june_mean_weather_data)
#print (north_july_mean_weather_data)
#print (north_aug_mean_weather_data)

#calAvg (north_june_df)
#print (calAvg (north_june_df))

#print(calMeanWeatherData(northDataFilter('North', 6, 2023)))

# plotting graph for all regions
# 1. North Region 
# Plot june weather data (for basic reference) 
#print("Combine bar and line graph")
keys = calMeanWeatherData(dataFilter('North', 6, 2023)).keys()
values = calMeanWeatherData(dataFilter('North', 6, 2023)).values()
plt.title('Weather data for June in North Region')
plt.bar (keys, values)
#plt.show()

# Plot july weather data (for basic reference)
#print("Combine bar and line graph")
#keys = north_july_mean_weather_data.keys()
#values = north_july_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot aug weather data (for basic reference)
#print("Combine bar and line graph")
#keys = north_aug_mean_weather_data.keys()
#values = north_aug_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()


# 2. South Region
# Plot june weather data (for basic reference)
#print("Combine bar and line graph")
#keys = south_june_mean_weather_data.keys()
#values = south_june_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot july weather data (for basic reference)
#print("Combine bar and line graph")
#keys = south_july_mean_weather_data.keys()
#values = south_july_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot aug weather data (for basic reference)
#print("Combine bar and line graph")
#keys = south_aug_mean_weather_data.keys()
#values = south_aug_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()


# 3. Central Region
# Plot june weather data (for basic reference)
#print("Combine bar and line graph")
#keys = central_june_mean_weather_data.keys()
#values = central_june_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot july weather data (for basic reference)
#print("Combine bar and line graph")
#keys = central_july_mean_weather_data.keys()
#values = central_july_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot aug weather data (for basic reference)
#print("Combine bar and line graph")
#keys = central_aug_mean_weather_data.keys()
#values = central_aug_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()



# 4. East Region
# Plot june weather data (for basic reference)
#print("Combine bar and line graph")
#keys = east_june_mean_weather_data.keys()
#values = east_june_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot july weather data (for basic reference)
#print("Combine bar and line graph")
#keys = east_july_mean_weather_data.keys()
#values = east_july_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot aug weather data (for basic reference)
#print("Combine bar and line graph")
#keys = east_aug_mean_weather_data.keys()
#values = east_aug_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()


# 5. West Region
# Plot june weather data (for basic reference)
#print("Combine bar and line graph")
#keys = west_june_mean_weather_data.keys()
#values = west_june_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot july weather data (for basic reference)
#print("Combine bar and line graph")
#keys = west_july_mean_weather_data.keys()
#values = west_july_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()

# Plot aug weather data (for basic reference)
#print("Combine bar and line graph")
#keys = west_aug_mean_weather_data.keys()
#values = west_aug_mean_weather_data.values()
#plt.bar (keys, values)
#plt.show()


# plot june weather data using seaborn
# figure 

# convert Dataframe to Dictionary
#dict_df = df.to_dict()
#print (dict_df)
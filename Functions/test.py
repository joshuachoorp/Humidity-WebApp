import os
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import datetime as datetime
import numpy as np


# Function to read csv file
#def readFile(file = (os.getcwd() + "/Datasets/combinedRegionData.csv")):
def readFile(file = "combinedRegionData.csv"):

    # Read csv file into Pandas Dataframe
    df = pd.read_csv(file, encoding="unicode-escape", usecols=[0,1,2,3,4,5,6,7])
    pd.set_option('display.max_columns', None)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    return df

# Read csv file
df = readFile()

test = [3, 2, 1]
label_df = df.loc[(df['Date'].dt.month == 8) & (df['Region'] == "North")]
labelDates = label_df['Date'].dt.strftime("%d").unique().tolist()
labelDates.sort()
print(labelDates)
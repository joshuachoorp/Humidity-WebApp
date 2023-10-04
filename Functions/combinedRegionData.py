import os
import time
import datetime as datetime
from bs4 import BeautifulSoup as BS
from selenium import webdriver
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
def render(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    driver.quit()
    return r

def scrape(station, date):
    output = pd.DataFrame()
    url = 'https://www.wunderground.com/dashboard/pws/%s/table/%s/%s/monthly' % (station, date, date)
    r = render(url)
    soup = BS(r, 'html.parser', )
    container = soup.find('lib-history-table')
    checkall = container.find_all('tbody')
    checkdate = checkall[0]
    checkdata = checkall[1]
    dates = []
    for i in checkdate.find_all('tr'):
        trial = i.get_text()
        trialconverted = datetime.datetime.strptime(trial, '%m/%d/%Y')
        dates.append(trialconverted.strftime("%d/%m/%Y"))

    # Iterate through span tags and get data
    data = []
    for i in checkdata.find_all('span', class_='wu-unit-humidity'):
        trial = i.get_text()
        removepercent = str(trial).replace('\xa0°%','')
        data.append(removepercent)
    columns = ['Humidity_High', 'Humidity_Avg', 'Humidity_Low']

    # Convert list of data to an array
    data_array = np.array(data, dtype=float)
    data_array = data_array.reshape(-1, len(columns))

    # Convert to dataframe
    df = pd.DataFrame(index=dates, data=data_array, columns=columns)
    conditions = [
        (station == 'ISINGA36'),
        (station == 'ISINGA112'),
        (station == 'ISINGAPO73'),
        (station == 'ISINGA167'),
        (station == 'ISINGA128'),
    ]
    region = ['North','South','Central','West','East']
    df['Region'] = np.select(conditions,region)

    return df

def combinedcsv():
    degree_sign = u"\N{DEGREE SIGN}"
    columns = ['Mean Temperature (°C)', 'Maximum Temperature (°C)', 'Lowest Temperature (°C)', 'Mean Wind Speed (km/h)',
               'Max Wind Speed (km/h)']

    regionData = pd.read_csv("../Datasets/RegionData.csv", encoding="unicode-escape", index_col="Date")
    northDF = pd.read_csv("../Datasets/Admiralty_data.csv", encoding="unicode-escape", index_col="Date")
    southDF = pd.read_csv("../Datasets/Sentosa Island_data.csv", encoding="unicode-escape", index_col="Date")
    centralDF = pd.read_csv("../Datasets/Ang Mo Kio_data.csv", encoding="unicode-escape", index_col="Date")
    eastDF = pd.read_csv("../Datasets/East Coast Parkway_data.csv", encoding="unicode-escape", index_col="Date")
    westDF = pd.read_csv("../Datasets/Tengah_data.csv", encoding="unicode-escape", index_col="Date")

    for i in columns:
        regionData.loc[regionData['Region'] == "North", i] = northDF[i]
        regionData.loc[regionData['Region'] == "South", i] = southDF[i]
        regionData.loc[regionData['Region'] == "Central", i] = centralDF[i]
        regionData.loc[regionData['Region'] == "East", i] = eastDF[i]
        regionData.loc[regionData['Region'] == "West", i] = westDF[i]
    return regionData.to_csv("../Datasets/compiledRegionData.csv")


# station = ['ISINGA36', 'ISINGA112', 'ISINGAPO73', 'ISINGA167', 'ISINGA128']
# dates = ['2023-06-10', '2023-07-10', '2023-08-10']
# for s in station:
#    for x in dates:
#        scrape(s, x).to_csv("RegionData.csv", mode="a", header=(not os.path.exists("RegionData.csv")))
#        #to prevent Headers from repeating

combinedcsv()

df = pd.read_csv("compiledRegionData.csv",encoding="unicode-escape")
figure = sns.lineplot(data=df, x="Mean Temperature (Â°C)", y="Humidity_Avg", hue="Region", style="Region",markers=True)
plt.show()
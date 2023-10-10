"""
Humidity Prediction
"""

import os
import pandas as pd
# Data visualization
import pmdarima as pm
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import seaborn as sns
import math
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
import warnings
from prophet import Prophet
from scipy import stats
from statsmodels.tsa.stattools import adfuller
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
import numpy as np
from sklearn.preprocessing import LabelEncoder
import mplcursors
from sklearn.linear_model import LinearRegression

def correlation():
    # Visualise correlation
    columns = ['Humidity_Avg', 'Mean Temperature (°C)', 'Mean Wind Speed (km/h)']
    corr = df[columns].corr()
    corr.rename(columns={'Humidity_Avg': 'Mean Humidity'}, inplace=True)
    plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", vmin=0, vmax=1)
    plt.title("Correlation between mean Humidity, Temperature and Wind Speed")
    return plt


def linear_regression():
    df['Mean Temperature (°C)'] = pd.to_numeric(df['Mean Temperature (°C)'], errors='coerce')
    df['Humidity_Avg'] = pd.to_numeric(df['Humidity_Avg'], errors='coerce')
    df['Mean Wind Speed (km/h)'] = pd.to_numeric(df['Mean Wind Speed (km/h)'], errors='coerce')

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Linear Regression for Mean Temperature vs. Mean Humidity
    x1 = np.array(df['Mean Temperature (°C)']).reshape(-1, 1)
    y = df['Humidity_Avg']
    model1 = LinearRegression()
    model1.fit(x1, y)
    y_pred1 = model1.predict(x1)

    ax1.scatter(x1, y, label='Actual Data', color='blue')
    ax1.plot(x1, y_pred1, label='Linear Regression Line', color='red')
    ax1.set_xlabel('Mean Temperature (°C)')
    ax1.set_ylabel('Humidity_Avg')
    ax1.set_title('Linear Regression: Humidity vs. Mean Temperature')
    ax1.legend()

    # Linear Regression for Mean Wind Speed vs. Mean Humidity
    x2 = np.array(df['Mean Wind Speed (km/h)']).reshape(-1, 1)
    model2 = LinearRegression()
    model2.fit(x2, y)
    y_pred2 = model2.predict(x2)

    ax2.scatter(x2, y, label='Actual Data', color='blue')
    ax2.plot(x2, y_pred2, label='Linear Regression Line', color='red')
    ax2.set_xlabel('Mean Wind Speed (km/h)')
    ax2.set_ylabel('Humidity_Avg')
    ax2.set_title('Linear Regression: Humidity vs. Mean Wind Speed (First Difference)')
    ax2.legend()

    plt.tight_layout()  # Ensure proper spacing between subplots
    return plt


def overview_data():
    # Read the combined data from the CSV file
    df = pd.read_csv(os.getcwd() + "/Datasets/combinedRegionData.csv", encoding="unicode-escape")
    #df = pd.read_csv("combinedRegionData.csv", encoding="unicode-escape")

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df.drop(columns=['Humidity_High', 'Humidity_Low', 'Maximum Temperature (°C)',
                    'Lowest Temperature (°C)', 'Max Wind Speed (km/h)'], axis=1, inplace=True)
    # Replace "-" with NaN in specific columns
    columns_with_nan = ['Humidity_Avg', 'Mean Temperature (°C)', 'Mean Wind Speed (km/h)']
    df[columns_with_nan] = df[columns_with_nan].replace('-', np.nan)
    df['Mean Temperature (°C)'] = pd.to_numeric(df['Mean Temperature (°C)'], errors='coerce')
    df['Mean Wind Speed (km/h)'] = pd.to_numeric(df['Mean Wind Speed (km/h)'], errors='coerce')

    # Drop rows containing NaN values in the specified columns
    df.dropna(subset=columns_with_nan, axis=0, inplace=True)

    # Plotting each of the time series
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    for i, column in enumerate(columns_with_nan):
        for region in df['Region'].unique():
            region_data = df[df['Region'] == region]
            sns.lineplot(x=region_data['Date'], y=region_data[column], ax=ax[i], label=region)
        if ax[i] == ax[0]:
            ax[0].set_title("Mean Humidity (%)", fontsize=14)
        else:
            ax[i].set_title(column, fontsize=14)
        ax[i].set_ylabel(ylabel=column, fontsize=10)
        ax[i].legend(title='Region', loc='upper right')
    plt.tight_layout()
    return plt

def visualize_adfuller_results(series, title, ax):
    result = adfuller(series)
    significance_level = 0.05
    adf_stat = result[0]
    p_val = result[1]
    crit_val_1 = result[4]['1%']
    crit_val_5 = result[4]['5%']
    crit_val_10 = result[4]['10%']
    # Determine custom y-axis tick locations only for 'Mean Wind Speed (km/h)'
    # Initialize a base palette with the default color
    base_palette = {
        "North": "blue",
        "South": "blue",
        "East": "blue",
        "West": "blue",
        "Central": "blue"
    }
    # Update the base palette based on conditions
    if (p_val < significance_level) and (adf_stat < crit_val_1):
        color = "forestgreen"
    elif (p_val < significance_level) and (adf_stat < crit_val_5):
        color = "orange"
    elif (p_val < significance_level) and (adf_stat < crit_val_10):
        color = "red"
    else:
        color = "purple"

    # Create the region_palette by updating the base_palette with the selected color
    region_palette = {region: color for region in base_palette}
    sns.lineplot(x=df['Date'], y=series, ax=ax, hue=df["Region"], palette=region_palette)
    ax.set_title(f'ADF Statistic {adf_stat:0.3f}, p-value: {p_val:0.3f}\nCritical Values 1%: {crit_val_1:0.3f}, 5%: {crit_val_5:0.3f}, 10%: {crit_val_10:0.3f}', fontsize=14)
    ax.set_ylabel(ylabel=title, fontsize=14)
    ax.legend(title='Region', loc='upper right')

# To show ADF Test results
def display_adf(df):
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    visualize_adfuller_results(df['Humidity_Avg'].values, 'Humidity_Avg', ax[0])
    visualize_adfuller_results(df['Mean Temperature (°C)'].values, 'Mean Temperature (°C)', ax[1])
    visualize_adfuller_results(df['Mean Wind Speed (km/h)'].values, 'Mean Wind Speed (km/h)', ax[2])
    plt.tight_layout()

def prophet_for_region(region_name, axs, train_size):
    # Filter the DataFrame for the specified region
    region_df = df[df['Region'] == region_name].copy()

    label_encoder = LabelEncoder()
    region_df['Region'] = label_encoder.fit_transform(region_df['Region'])

    # Prepare the DataFrame for Prophet
    features = ['Mean Temperature (°C)', 'First_Difference_Wind']
    target = ['Humidity_Avg']
    multivariate_df = region_df[['Date'] + target + features + ['Region']].copy()
    multivariate_df.columns = ['ds', 'y'] + features + ['Region']
    train = multivariate_df.iloc[:train_size, :]
    # divide train_size by 5 due to the 5 regions. This is to ensure that the train and test set are of the same size
    x_train, y_train = pd.DataFrame(multivariate_df.iloc[:int(train_size/5), [0, 2, 3]]), pd.DataFrame(multivariate_df.iloc[:int(train_size/5), 1])
    x_valid, y_valid = pd.DataFrame(multivariate_df.iloc[int(train_size/5):, [0, 2, 3]]), pd.DataFrame(multivariate_df.iloc[int(train_size/5):, 1])

    model = Prophet()
    model.add_regressor('Mean Temperature (°C)')
    model.add_regressor('First_Difference_Wind')
    model.fit(train)

    # Predict on valid set
    y_pred = model.predict(x_valid)
    # Calculate metrics
    score_mae = mean_absolute_error(y_valid, y_pred['yhat'])
    score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred['yhat']))
    model.plot(y_pred, ax=axs)

    future_dates = model.make_future_dataframe(periods=30)
    future_dates[features[0]] = df['Mean Temperature (°C)']
    future_dates[features[1]] = df['First_Difference_Wind']
    # Predict for future dates
    forecast = model.predict(future_dates)
    # Plot the forecast
    train_plot = sns.lineplot(x=x_train['ds'], y=y_train['y'], ax=axs, color='red', label='Train Set')
    ground_truth_plot = sns.lineplot(x=x_valid['ds'], y=y_valid['y'], ax=axs, color='orange', label='Ground truth', ci=None)
    forecast_plot = model.plot(forecast, ax=axs)
    axs.set_title(f'Prediction of the next month for {region_name} region\nMAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=10)
    axs.set_xlabel(xlabel='Date', fontsize=10)
    axs.set_ylabel(ylabel='Humidity', fontsize=10)
    axs.legend(title='Legend', loc='upper left')
    mplcursors.cursor([train_plot, ground_truth_plot, forecast_plot])
    plt.tight_layout()
    return plt


# Read the combined data from the CSV file
df = pd.read_csv(os.getcwd() + "/Datasets/combinedRegionData.csv", encoding="unicode-escape")
#df = pd.read_csv("combinedRegionData.csv", encoding="unicode-escape")

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df.drop(columns=['Humidity_High', 'Humidity_Low', 'Maximum Temperature (°C)',
                 'Lowest Temperature (°C)', 'Max Wind Speed (km/h)'], axis=1, inplace=True)
# Replace "-" with NaN in specific columns
columns_with_nan = ['Humidity_Avg', 'Mean Temperature (°C)', 'Mean Wind Speed (km/h)']
df[columns_with_nan] = df[columns_with_nan].replace('-', np.nan)

# Drop rows containing NaN values in the specified columns
df.dropna(subset=columns_with_nan, inplace=True)


#linear_regression()
#overview_data()
#correlation()
#display_adf(df)

def predictionHumidity():
    df['Mean Wind Speed (km/h)'] = pd.to_numeric(df['Mean Wind Speed (km/h)'], errors='coerce')
    df['First_Difference_Wind'] = pd.to_numeric(df['Mean Wind Speed (km/h)'], errors='coerce')
    df['First_Difference_Wind'] = df['Mean Wind Speed (km/h)'].diff()
    df['First_Difference_Wind'].fillna(0, inplace=True)

    # Perform the ADF test on the differenced time series
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 8))
    visualize_adfuller_results(df['First_Difference_Wind'], 'First_Difference_Wind', ax)
    plt.tight_layout()

    # Split the data into train and test sets
    train_size = int(0.90 * len(df))
    # Define the regions you want to predict
    regions_to_predict = ['North', 'South', 'East', 'West', 'Central']
    fig, axs = plt.subplots(len(regions_to_predict), 1, figsize=(20, 12))
    # Loop through regions and make predictions for each one
    for i, region in enumerate(regions_to_predict):
        predictionGraphs = prophet_for_region(region, axs[i], train_size)
    return predictionGraphs


#predictionHumidity()
#plt.show()

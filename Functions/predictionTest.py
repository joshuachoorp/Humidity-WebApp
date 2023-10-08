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

# Read the combined data from the CSV file
#df = pd.read_csv(os.getcwd() + "/Datasets/compiledRegionData.csv", encoding="unicode-escape")
df = pd.read_csv("combinedRegionData.csv", encoding="unicode-escape")
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df.drop(columns=['Humidity_High', 'Humidity_Low', 'Maximum Temperature (°C)',
                 'Lowest Temperature (°C)', 'Max Wind Speed (km/h)'], axis=1, inplace=True)

# Replace "-" with NaN in specific columns
columns_with_nan = ['Humidity_Avg', 'Mean Temperature (°C)', 'Mean Wind Speed (km/h)']
df[columns_with_nan] = df[columns_with_nan].replace('-', np.nan)

# Drop rows containing NaN values in the specified columns
df.dropna(subset=columns_with_nan, inplace=True)


def correlation():
    # Visualise correlation
    columns = ['Humidity_Avg', 'Mean Temperature (°C)', 'Mean Wind Speed (km/h)']
    corr = df[columns].corr()
    corr.rename(columns={'Humidity_Avg': 'Mean Humidity'}, inplace=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    heatmap = sns.heatmap(corr, annot=True, fmt=".2f", vmin=0, vmax=1)
    heatmap.set_ylabel('Humidity')
    plt.title("Correlation between mean Humidity, Temperature and Wind Speed")
    return plt

def linear_regression():
    df['Mean Temperature (°C)'] = pd.to_numeric(df['Mean Temperature (°C)'], errors='coerce')
    df['Humidity_Avg'] = pd.to_numeric(df['Humidity_Avg'], errors='coerce')
    x = np.array(df['Mean Temperature (°C)']).reshape(-1, 1)
    y = df['Humidity_Avg']
    model = LinearRegression()
    # Fit the model to the data
    model.fit(x, y)
    x = x.tolist()

    # Make predictions using the trained model
    y_pred = model.predict(x)

    # Visualize the linear regression line and the actual data points
    plt.scatter(x, y, label='Actual Data', color='blue')
    plt.plot(x, y_pred, label='Linear Regression Line', color='red')
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Humidity_Avg')
    plt.title('Linear Regression: Humidity vs. Mean Temperature')
    plt.legend()
    return plt

def overview_data():
    # Plotting each of the time series
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    sns.despine()
    # Get the columns you want to plot (excluding 'Date' and 'Region')
    columns_to_plot = df.drop(['Date', 'Region'], axis=1).columns

    for i, column in enumerate(columns_to_plot):
        for region in df['Region'].unique():
            region_data = df[df['Region'] == region]
            sns.lineplot(x=region_data['Date'], y=region_data[column], ax=ax[i], label=region)

        ax[i].set_title('Feature: {}'.format(column), fontsize=14)
        ax[i].set_ylabel(ylabel=column, fontsize=10)
        ax[i].legend(title='Region', loc='upper right')
        if i == 2:
            ax[i].invert_yaxis()
            ax[i].set_yticks([10,20,30,40,50,60,70,80,90,100])
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
    if title == 'Mean Wind Speed (km/h)':
        y_ticks = [10,20,30,40,50,60,70,80,90,100]  # Customize these values as needed
        ax.set_yticks(y_ticks)  # Set custom y-axis ticks
    else:
        y_ticks = None  # Default ticks for other titles
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
    features = ['Mean Temperature (°C)', 'Second_Difference_Wind']
    target = ['First_Difference_Humidity']
    multivariate_df = region_df[['Date'] + target + features + ['Region']].copy()
    multivariate_df.columns = ['ds', 'y'] + features + ['Region']
    train = multivariate_df.iloc[:train_size, :]
    x_train, y_train = pd.DataFrame(multivariate_df.iloc[:50, [0, 2, 3]]), pd.DataFrame(multivariate_df.iloc[:50, 1])
    x_valid, y_valid = pd.DataFrame(multivariate_df.iloc[50:, [0, 2, 3]]), pd.DataFrame(multivariate_df.iloc[50:, 1])

    model = Prophet()
    model.add_regressor('Mean Temperature (°C)')
    model.add_regressor('Second_Difference_Wind')
    model.fit(train)

    # Predict on valid set
    y_pred = model.predict(x_valid)
    # Calculate metrics
    score_mae = mean_absolute_error(y_valid, y_pred['yhat'])
    score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred['yhat']))
    model.plot(y_pred, ax=axs)

    future_dates = model.make_future_dataframe(periods=89)
    future_dates[features[0]] = df['Mean Temperature (°C)']
    future_dates[features[1]] = df['Second_Difference_Wind']
    future_dates['Second_Difference_Wind'].fillna(0, inplace=True)
    # Predict for future dates
    forecast = model.predict(future_dates)
    # Plot the forecast
    train_plot = sns.lineplot(x=x_train['ds'], y=y_train['y'], ax=axs, color='red', label='Train Set')
    ground_truth_plot = sns.lineplot(x=x_valid['ds'], y=y_valid['y'], ax=axs, color='orange', label='Ground truth', ci=None)
    forecast_plot = model.plot(forecast, ax=axs)
    axs.set_title(f'Prediction of the next 3 months for {region_name} region\nMAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=10)
    axs.set_xlabel(xlabel='Date', fontsize=10)
    axs.set_ylabel(ylabel='Humidity', fontsize=10)
    mplcursors.cursor([train_plot, ground_truth_plot, forecast_plot])
    plt.tight_layout()







df['Humidity_Avg'] = pd.to_numeric(df['Humidity_Avg'], errors='coerce')
df['Mean Wind Speed (km/h)'] = pd.to_numeric(df['Mean Wind Speed (km/h)'], errors='coerce')
df['First_Difference_Humidity'] = df['Humidity_Avg'].diff().dropna()  # Remove NaN resulting from differencing
df['Second_Difference_Wind'] = df['Mean Wind Speed (km/h)'].diff().dropna()  # Remove NaN resulting from differencing


# Perform the ADF test on the differenced time series
fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))
visualize_adfuller_results(df['First_Difference_Humidity'].dropna(), 'First_Difference_Humidity', ax[0])
visualize_adfuller_results(df['Second_Difference_Wind'].dropna(), 'Second_Difference_Wind', ax[1])
plt.tight_layout()

def predictionHumidity():
    # Split the data into train and test sets
    train_size = int(0.50 * len(df))
    # Define the regions you want to predict
    regions_to_predict = ['North', 'South', 'East', 'West', 'Central']
    fig, axs = plt.subplots(len(regions_to_predict), 1, figsize=(20, 12))

    # Loop through regions and make predictions for each one
    for i, region in enumerate(regions_to_predict):
        predictionGraphs = prophet_for_region(region, axs[i], train_size)
    predictionGraphs.show()
    return predictionGraphs

#linear_regression(df)
#correlation(df)
#overview_data(df)
#display_adf(df)
#predictionHumidity().show()
correlation().show()
plt.show()

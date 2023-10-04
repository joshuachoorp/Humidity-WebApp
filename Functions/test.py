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
from sklearn.preprocessing import LabelEncoder
import mplcursors

# Check for missing values in dataframe:
def missingvalues():
    dict = {}
    for i in list(df.columns):
        dict[i] = (df[i].isnull().sum(), round(df[i].isnull().sum() / len(df) * 100, 2))
    print(pd.DataFrame(dict, index=["# of missing values", "% of missing values"]).transpose().sort_values(by=["# of missing values"], ascending=False))

# # Function to visualize Augmented Dickey–Fuller test
def visualize_adfuller_results(series, title, ax):
    result = adfuller(series)
    significance_level = 0.05
    adf_stat = result[0]
    p_val = result[1]
    crit_val_1 = result[4]['1%']
    crit_val_5 = result[4]['5%']
    crit_val_10 = result[4]['10%']
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

def prophet_for_region(region_name, axs):
    # Filter the DataFrame for the specified region
    region_df = df[df['Region'] == region_name].copy()

    label_encoder = LabelEncoder()
    region_df['Region'] = label_encoder.fit_transform(region_df['Region'])

    # Prepare the DataFrame for Prophet
    features = ['Mean Temperature (Â°C)']
    target = ['Humidity_Avg']
    multivariate_df = region_df[['Date'] + target + features + ['Region']].copy()
    multivariate_df.columns = ['ds', 'y'] + features + ['Region']

    train = multivariate_df.iloc[:train_size, :]
    x_train, y_train = pd.DataFrame(multivariate_df.iloc[:50, [0, 2]]), pd.DataFrame(multivariate_df.iloc[:50, 1])
    x_valid, y_valid = pd.DataFrame(multivariate_df.iloc[50:, [0, 2]]), pd.DataFrame(multivariate_df.iloc[50:, 1])

    model = Prophet()
    model.add_regressor('Mean Temperature (Â°C)')
    model.fit(train)

    # Predict on valid set
    y_pred = model.predict(x_valid)
    # Calculate metrics
    score_mae = mean_absolute_error(y_valid, y_pred['yhat'])
    score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred['yhat']))
    model.plot(y_pred, ax=axs[0])
    # Plot training set and ground truth
    train_plot = sns.lineplot(x=x_train['ds'], y=y_train['y'], ax=axs[0], color='red', label='Train Set')
    ground_truth_plot = sns.lineplot(x=x_valid['ds'], y=y_valid['y'], ax=axs[0], color='orange', label='Ground truth')
    axs[0].legend(loc='lower left', fontsize=8)
    axs[0].set_title(f'Training Set: {region_name}\nMAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=10)
    axs[0].set_xlabel(xlabel='Date', fontsize=10)
    axs[0].set_ylabel(ylabel='Humidity', fontsize=10)

    future_dates = model.make_future_dataframe(periods=90)
    future_dates[features[0]] = df['Mean Temperature (Â°C)']
    # Predict for future dates
    forecast = model.predict(future_dates)
    # Plot the forecast
    sns.lineplot(x=x_train['ds'], y=y_train['y'], ax=axs[1], color='red', label='Train Set')
    sns.lineplot(x=x_valid['ds'], y=y_valid['y'], ax=axs[1], color='orange', label='Ground truth', ci=None)
    forecast_plot = model.plot(forecast, ax=axs[1])
    forecast_plot.set_label('Forecast')
    axs[1].legend(loc='lower left', fontsize=8)
    axs[1].set_title(f'Prediction for the next 3 months for {region_name} region\nMAE: {score_mae:.2f}, RMSE: {score_rmse:.2f}', fontsize=10)
    axs[1].set_xlabel(xlabel='Date', fontsize=10)
    axs[1].set_ylabel(ylabel='Humidity', fontsize=10)
    mplcursors.cursor([train_plot, ground_truth_plot,forecast_plot])

    plt.tight_layout()

df = pd.read_csv((os.getcwd() + "/Datasets/compiledRegionData.csv"), encoding="unicode-escape")
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df.drop(columns=['Humidity_High', 'Humidity_Low', 'Maximum Temperature (Â°C)',
                 'Lowest Temperature (Â°C)', 'Max Wind Speed (km/h)'], axis=1, inplace=True)

x = df['Mean Temperature (Â°C)']
y = df['Humidity_Avg']
slope, intercept, r, p, std_err = stats.linregress(x, y)
# create a function that makes use of the slope and intercept to provide new values.
def myfunc(x):
  return slope * x + intercept
# linear regression




def scatterPlot():
    # to create a new array with new values on the y-axis, run each value of the x array through the function
    mymodel = list(map(myfunc, x))
    # draw the scatter plot
    plt.scatter(x, y)
    # draw the line of regression
    plt.plot(x, mymodel, color="red")

    # label the x axis and y axis
    plt.xlabel('Temperature')
    plt.ylabel('Humidity')
    plt.title("Linear Regression between Humidity and Temperature")
    return plt

def correlation():
# Visualise correlation
    columns = ['Mean Temperature (Â°C)', 'Humidity_Avg', 'Mean Wind Speed (km/h)']
    corr = df[columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", vmin=0, vmax=1)
    plt.title("Correlation between mean Temperature, Humidity and Wind Speed")
    return plt

# Plotting each of the time series
fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
sns.despine()

# Get the columns you want to plot (excluding 'Date' and 'Region')
columns_to_plot = df.drop(['Date', 'Region'], axis=1).columns

def feature():
    for i, column in enumerate(columns_to_plot):
        for region in df['Region'].unique():
            region_data = df[df['Region'] == region]
            sns.lineplot(x=region_data['Date'], y=region_data[column], ax=ax[i], label=region)

        ax[i].set_title('Feature: {}'.format(column), fontsize=14)
        ax[i].set_ylabel(ylabel=column, fontsize=10)
        ax[i].legend(title='Region', loc='upper left')
    plt.tight_layout()
    return plt

def adfResults():
    # To show ADF Test results
    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    visualize_adfuller_results(df['Humidity_Avg'].values, 'Humidity_Avg', ax[0])
    visualize_adfuller_results(df['Mean Temperature (Â°C)'].values, 'Mean Temperature (Â°C)', ax[1])
    visualize_adfuller_results(df['Mean Wind Speed (km/h)'].values, 'Mean Wind Speed (km/h)', ax[2])
    plt.tight_layout()
    return plt

train_size = int(0.90 * len(df))
def prophet_for_region(region_name, axs):
    # Filter the DataFrame for the specified region
    region_df = df[df['Region'] == region_name].copy()

    label_encoder = LabelEncoder()
    region_df['Region'] = label_encoder.fit_transform(region_df['Region'])

    # Prepare the DataFrame for Prophet
    features = ['Mean Temperature (Â°C)']
    target = ['Humidity_Avg']
    multivariate_df = region_df[['Date'] + target + features + ['Region']].copy()
    multivariate_df.columns = ['ds', 'y'] + features + ['Region']

    train = multivariate_df.iloc[:train_size, :]
    x_train, y_train = pd.DataFrame(multivariate_df.iloc[:50, [0, 2]]), pd.DataFrame(multivariate_df.iloc[:50, 1])
    x_valid, y_valid = pd.DataFrame(multivariate_df.iloc[50:, [0, 2]]), pd.DataFrame(multivariate_df.iloc[50:, 1])

    model = Prophet()
    model.add_regressor('Mean Temperature (Â°C)')
    model.fit(train)

    # Predict on valid set
    y_pred = model.predict(x_valid)
    # Calculate metrics
    score_mae = mean_absolute_error(y_valid, y_pred['yhat'])
    score_rmse = math.sqrt(mean_squared_error(y_valid, y_pred['yhat']))
    model.plot(y_pred, ax=axs)

    future_dates = model.make_future_dataframe(periods=90)
    future_dates[features[0]] = df['Mean Temperature (Â°C)']
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


train_size = int(0.50 * len(df))
df = pd.read_csv((os.getcwd() + "/Datasets/compiledRegionData.csv"), encoding="unicode-escape")
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

# Define the regions you want to predict
regions_to_predict = ['North', 'South', 'East', 'West', 'Central']
fig, axs = plt.subplots(len(regions_to_predict), 1, figsize=(20, 12))

def humidityPrediction():
    # Loop through regions and make predictions for each one
    for i, region in enumerate(regions_to_predict):
        prophet_for_region(region, axs[i])
    return plt


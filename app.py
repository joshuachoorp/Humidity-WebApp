"""
Flask backend of Humidity-Webapp
"""

# Check for required libraries in the system
# Will Download libraries from requirements.txt if any libraries not found
from testRequirements import checkReq
checkReq()

# Imports from PlotWeather file
from Functions import dataGroup, dataPlot, canvasName, dataCreateDiv

# Imports from Prediction file
from Functions import linear_regression, correlation, overview_data, predictionHumidity

# Imports from 
from Functions import month_name_filter

from pathlib import Path
import base64
import os
from io import BytesIO

from flask import Flask, jsonify, render_template, request, redirect, flash, send_file, send_from_directory, current_app, abort
import flask
import pandas as pd
import numpy as np



if __name__ == '__main__':
    while True:
        # Checks for required packages and installs them if not found
        try:
            from app import app
            #app.run(debug=True)
            app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))

        except Exception as e:
            print(e)
            break

        break

# Register the custom filter function
app = Flask(__name__, static_folder='Static', template_folder='template')
app.jinja_env.filters['month_name'] = month_name_filter
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Index Page
@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# Exports chart to backend Downloads folder
@app.route('/dashboard/download', methods=['GET', 'POST'])
def downloadBackEnd():
    # Retrieve data sent by js file
    barChartBase64 = request.form['graphBase64']
    barChartName = request.form['graphName']

    # Remove header of base64 string
    barChartBase64 = barChartBase64.replace('data:image/png;base64,', '')

    # Writing base64 string to png file to show image of graph
    with open(os.getcwd() + "/Downloads/" + barChartName + ".png", "wb") as fh:
        fh.write(base64.b64decode(barChartBase64))

    print(os.listdir(os.getcwd() + "/Downloads/"))
    print(os.listdir(os.getcwd()))
    # Adding file type to input chart
    chartName = barChartName + ".png"

    return redirect('/dashboard/' + chartName)


# Allow users to download image of chart 
@app.route('/dashboard/<filename>', methods=['GET'])
def downloadFile(filename):

    # Locate the current working directory and go to Downloads folder
    filepath = os.getcwd() + "/Downloads/"

    # Try to download the file
    try:
        # Download image of graph to local user
        return send_file(filepath + filename, as_attachment=True)

    # FileNotFoundError
    except Exception as e:
        return jsonify({'error': str(e)})


# Table view page
# Shows contents of csv file
@app.route('/table/')
def table():
    data = pd.read_csv('Datasets/combinedRegionData.csv', encoding='latin1')
    data_dict_list = data.to_dict(orient='records')
    headers = data.columns.tolist()
    return render_template('table.html', headers=headers, data = data_dict_list)


# Prediction Page
# Shows contents of csv file
@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    #Back button to main page
    if request.form.get('back') == 'back':
        return redirect('/')

    predictionGraph = convertGraphToB64(predictionHumidity())
    correlationGraph = convertGraphToB64(correlation())
    overviewGraph = convertGraphToB64(overview_data())
    linearGraph = convertGraphToB64(linear_regression())

    return render_template('Prediction.html',
                           prediction=predictionGraph,
                           correlationGraph=correlationGraph,
                           overview=overviewGraph,
                           linear=linearGraph)


# North Region Page
# Show graphs and data related to North region
@app.route("/North")
def North():
    # Data for North Region
    chartObj = dataCreateDiv("North")
    return render_template('North.html', createDiv=chartObj)


# South Region Page
# Show graphs and data related to South region
@app.route("/South")
def South():
    # Data for South Region
    chartObj = dataCreateDiv("South")
    return render_template('South.html', createDiv=chartObj)


# Central Region Page
# Show graphs and data related to Central region
@app.route("/Central")
def Central():
    # Data for Central Region
    chartObj = dataCreateDiv("Central")
    return render_template('Central.html', createDiv=chartObj)


# East Region Page
# Show graphs and data related to East region
@app.route("/East")
def East():
    # Data for East Region
    chartObj = dataCreateDiv("East")
    return render_template('East.html', createDiv=chartObj)


# West Region Page
# Show graphs and data related to West region
@app.route("/West")
def West():
    # Data for West Region
    chartObj = dataCreateDiv("West")

    return render_template('West.html', createDiv=chartObj)



# Export dataset as csv
# Allow users to download csv file we used
@app.route("/ExportFile")
def exportFile():

    filepath = os.getcwd() + "\Datasets\combinedRegionData.csv"

    return send_file(filepath, as_attachment=True)



# Import file
# Allow users to import a csv file
@app.route('/process-csv', methods=['POST'])
def process_csv():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    #once confirm the header test.csv will change to the compileddata.csv
    csv_file_path = os.path.join(base_dir, 'Datasets', 'compiledRegionData.csv')
    try:
        # Get the uploaded file from the request
        file = request.files['file']
        selectRegion = request.form.get('region')
        # Validate the file extension 
        if file.filename.endswith(('.csv')):
            # Read the Excel file into a DataFrame
            try:
                df = pd.read_csv(file, encoding="unicode-escape")
                region_data = [selectRegion] * len(df)
                df.insert(4, 'Region', region_data)
            except UnicodeDecodeError as e:
                # Handle encoding issues
                return jsonify({'error': 'Encoding error: ' + str(e)})
            #Ensure that the path the always correct 
            if os.path.exists(csv_file_path):
                existing_df = pd.read_csv(csv_file_path)
            else:
            # Handle the case where the file does not exist
                return jsonify({'error': 'File does not exist'})             
            append_next = True  # Flag to indicate whether to append the next row
            new_rows = []

            for _, row in df.iterrows():
                if row.isnull().all() and append_next:
                    append_next = False
                elif not row.isnull().all() and append_next:
                    new_rows.append(row)
                    append_next = False
                elif not row.isnull().all() and not append_next:
                    new_rows.append(row)

            combined_df = pd.concat([existing_df, pd.DataFrame(new_rows)], ignore_index=True)
            combined_df.to_csv(csv_file_path,  mode='w', index=False)  # Overwrite the file
            app.logger.info(combined_df)
            # You can also return a response to the client if needed
            return jsonify({'message': 'Data processed and saved successfully'})
        else:
            return jsonify({'error': 'Invalid file format'})
    except Exception as e:
        return jsonify({'error': str(e)})







# Function to read csv file
def readCsv(csvFileName):
    # Reading data from csv file
    data = pd.read_csv(csvFileName, encoding='unicode_escape')
    return data


# Function to convert matplotlib graphs to base64 to be sent to html page
def convertGraphToB64(plot):
    img = BytesIO()
    plot.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plotB64 = base64.b64encode(img.getvalue()).decode('utf8')
    return plotB64


"""
Flask backend of Humidity-Webapp
"""
#Check for required libraries in the system
from testRequirements import checkReq
checkReq()
from Functions.Filters import month_name_filter
from pathlib import Path
import base64
import os
from io import BytesIO

#from Functions import PlotWeather
from Functions import dataGroup, dataPlot, canvasName, dataCreateDiv
from Functions import linear_regression, correlation, overview_data, predictionHumidity
from flask import Flask, render_template, request, redirect, flash, send_file, send_from_directory, current_app, abort
import flask
import pandas as pd
import numpy as np



if __name__ == '__main__':
    while True:
        # Checks for required packages and installs them if not found
        try:
            from app import app
            #app.run(debug=True)
            from werkzeug.serving import run_simple
            run_simple('127.0.0.1', 5000, app)

        # Checks for required packages and installs them if not found
        # If module required not installed, will throw exception.
        # If thrown exception, will install modules required based on requirements.txt
        except ModuleNotFoundError as e:
            checkReq()
            print(e)
            continue

        except Exception as e:
            print(e)
            break

        break

# Register the custom filter function


app = Flask(__name__,static_folder='Static')
app.jinja_env.filters['month_name'] = month_name_filter
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
# Index Page
@app.route('/index')
def index():

    return render_template('index.html')

@app.route("/")
def Home():
    return render_template('Dashboard.html')


# Creating dashboard
@app.route('/dashboard/', methods=['GET', 'POST'])
def plot():
    # Data for North Region
    #northGroup = dataGroup('North', 2023)

    # Data for South Region
    #southGroup = dataGroup('South', 2023)

    # Data for Central Region
    #centralGroup = dataGroup('Central', 2023)

    # Data for East Region
    #eastGroup = dataGroup('East', 2023)

    # Data for West Region
    #westGroup = dataGroup('West', 2023)


    # Passing data to dashboard
    if request.method == 'POST' and request.form.get('plot') == 'dashboard':
        pass
        #return render_template('graphs.html',
        #                       lineTitleNorth = northGroup[0], lineLabelNorth = northGroup[1], lineValueNorth = northGroup[2], canvasNorth = northGroup[3],
        #                       lineTitleSouth = southGroup[0], lineLabelSouth = southGroup[1], lineValueSouth = southGroup[2], canvasSouth = southGroup[3],
        #                       lineTitleCentral = centralGroup[0], lineLabelCentral = centralGroup[1], lineValueCentral = centralGroup[2], canvasCentral = centralGroup[3],
        #                       lineTitleEast = eastGroup[0], lineLabelEast = eastGroup[1], lineValueEast = eastGroup[2], canvasEast = eastGroup[3],
        #                       lineTitleWest = westGroup[0], lineLabelWest = westGroup[1], lineValueWest = westGroup[2], canvasWest = westGroup[3],)

    # Prevents access to dashboard through URL; Only can access through index page's button
    elif request.method == 'GET':
        return redirect('/')

    else:
        return 'Not a valid request method for this route'


# Exports chart to backend Downloads folder
@app.route('/dashboard/download', methods=['GET', 'POST'])
def downloadBackEnd():
    # Retrieve data sent by js file
    barChartBase64 = request.form['graphBase64']
    barChartName = request.form['graphName']

    # Remove header of base64 string
    barChartBase64 = barChartBase64.replace('data:image/png;base64,', '')

    # Writing base64 string to png file to show image of graph
    with open("Downloads\\" + barChartName + ".png", "wb") as fh:
        fh.write(base64.b64decode(barChartBase64))

    # Adding file type to input chart
    chartName = barChartName + ".png"

    return redirect('/dashboard/' + chartName)


# Allow users to download image of chart 
@app.route('/dashboard/<filename>', methods=['GET'])
def downloadFile(filename):

    # Locate the current working directory and go to Downloads folder
    filepath = os.getcwd() + "\Downloads\\"

    # Try to download the file
    try:
        # Download image of graph to local user
        return send_file(filepath + filename, as_attachment=True)

    # FileNotFoundError
    except FileNotFoundError:
        return abort(404)


# Table view page
# Shows contents of csv file
@app.route('/table/', methods=['GET', 'POST'])
def table():
    # Check for if file is uploaded
    if request.method == 'POST' and request.files['fileName'].filename == '':
        return redirect('/')

    elif request.method == 'POST':
        uploadFile = request.files['fileName']

        # Creating table for csv files 
        if uploadFile.filename.lower().endswith(('.csv')):
            data = readCsv(uploadFile)
            return render_template('table.html', tables=[data.to_html()], titles=[''])

        # Creating table for json files
        elif uploadFile.filename.lower().endswith(('.json')):
            return render_template('table.html')

        # Creating table for txt files
        elif uploadFile.filename.lower().endswith(('.txt')):
            return render_template('table.html')

        else:
            return redirect('/')

    # Back button to main page
    if request.method == 'POST' and request.form.get('back') == 'back':
        return redirect('/')

    # Only allow access to this page through the main page
    elif request.method == 'GET':
        return redirect('/')

    else:
        return 'Not a valid request method for this route'


# Prediction Page
# Shows contents of csv file
@app.route('/prediction', methods=['GET', 'POST'])
def predict():
    #Back button to main page
    if request.method == 'POST' and request.form.get('back') == 'back':
        return redirect('/')

    elif request.method == 'POST':
        #linear_regression().show()
        #correlation().show()
        #overview_data().show()
        #predictionHumidity().show()
        
        linearGraph = convertGraphToB64(linear_regression())
        predictionGraph = convertGraphToB64(predictionHumidity())
        correlationGraph = convertGraphToB64(correlation())
        #overviewGraph = convertGraphToB64(overview_data())

        return render_template('prediction.html', 
                               correlationGraph=correlationGraph,
                               prediction=predictionGraph,
                               #overview=overviewGraph,
                               linear = linearGraph)
    
    #Only allow access to this page through the main page
    elif request.method == 'GET':
        return redirect('/')




# Function to read csv file
def readCsv(csvFileName):
    # Reading data from csv file
    data = pd.read_csv(csvFileName, encoding='unicode_escape')
    return data


#Function to convert matplotlib graphs to base64 to be sent to html page
def convertGraphToB64(plot):
    img = BytesIO()
    plot.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    #plotB64 = base64.b64encode(img.getvalue()).decode('utf8')
    return base64.b64encode(img.getvalue()).decode('utf8')



@app.route("/North")
def North():
    chartObj = dataCreateDiv("North")
    return render_template('North.html', createDiv=chartObj)

@app.route("/South")
def South():
    chartObj = dataCreateDiv("South")
    return render_template('South.html', createDiv=chartObj)

@app.route("/East")
def East():
    chartObj = dataCreateDiv("East")
    return render_template('East.html', createDiv=chartObj)

@app.route("/West")
def West():
    chartObj = dataCreateDiv("West")
    return render_template('West.html', createDiv=chartObj)

@app.route("/Central")
def Central():
    chartObj = dataCreateDiv("Central")
    return render_template('Central.html', createDiv=chartObj)


# Export dataset as csv
# Allow users to download csv file we used
@app.route("/ExportFile")
def exportFile():

    filepath = os.getcwd() + "\Datasets\compiledRegionData.csv"

    return send_file(filepath, as_attachment=True)


# Import file
# Allow users to import a csv file
@app.route("/ImportFile")
def importFile():

    filepath = os.getcwd() + "\Datasets\compiledRegionData.csv"

    return send_file(filepath, as_attachment=True)



@app.route("/testPage")
def testPage():
    chartObj = dataCreateDiv("North")
    return render_template('testPage.html',
                           createDiv=chartObj)

from pathlib import Path
import base64
import os

from distutils.command import upload
from flask import Flask, render_template, request, redirect, flash, send_file, send_from_directory, current_app, abort
import flask
import pandas as pd

app = Flask(__name__,static_folder='Static')

# Index Page
@app.route('/')
def index():
    return render_template('index.html')


# Creating dashboard
@app.route('/dashboard/', methods=['GET', 'POST'])
def plot():
    # Data for Bar Chart
    label1 = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    values1 = [5, 4, 3, 2, 1]

    # Data for Line Graph
    label2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    values2 = [65, 59, 80, 81, 56, 55, 40]

    # Passing data to dashboard
    if request.method == 'POST' and request.form.get('plot') == 'dashboard':
        return render_template('graphs.html', chartLabel=label1, chartValue=values1, lineLabel = label2, lineValue = values2)
    
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



#Table view
#Shows contents of csv file
@app.route('/table/', methods=['GET', 'POST'])
def table():
    #Check for if file is uploaded
    if request.method == 'POST' and request.files['fileName'].filename == '':
        return redirect('/')
    
    elif request.method == 'POST':
        uploadFile = request.files['fileName']
        
        #Creating table for csv files 
        if uploadFile.filename.lower().endswith(('.csv')):
            data = readCsv(uploadFile)
            return render_template('table.html', tables=[data.to_html()], titles=[''])
        
        #Creating table for json files
        elif uploadFile.filename.lower().endswith(('.json')):
            return render_template('table.html')
        
        #Creating table for txt files
        elif uploadFile.filename.lower().endswith(('.txt')):
            return render_template('table.html')
        
        else:
            return redirect('/')
        
    #Back button to main page
    if request.method == 'POST' and request.form.get('back') == 'back':
        return redirect('/')
    
    #Only allow access to this page through the main page
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        return 'Not a valid request method for this route'
    

#Function to read csv file
def readCsv(csvFileName):
    data = pd.read_csv(csvFileName, encoding='unicode_escape')

    return data


@app.route("/Home")
def Home():
    return render_template("Dashboard.html")


#if __name__ == '__main__':
#    checkReq()
#    app.run(debug=True)
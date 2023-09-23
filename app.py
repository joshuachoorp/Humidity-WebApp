from distutils.command import upload
from flask import Flask, render_template, request, redirect, flash
import flask
import pandas as pd
from testRequirements import checkReq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/dashboard/', methods=['POST'])
def plot():
    # Data for Bar Chart
    label1 = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    values1 = [5, 4, 3, 2, 1]

    # Data for Line Graph
    label2 = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    values2 = [65, 59, 80, 81, 56, 55, 40]

    if request.method == 'POST' and request.form.get('plot') == 'dashboard':
        return render_template('graphs.html', chartLabel=label1, chartValue=values1, lineLabel = label2, lineValue = values2)
    
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        return 'Not a valid request method for this route'



@app.route('/table/', methods=['GET', 'POST'])
def table():

    if request.method == 'POST' and request.files['fileName'].filename == '':
        return redirect('/')
    
    elif request.method == 'POST':
        uploadFile = request.files['fileName']
        
        if uploadFile.filename.lower().endswith(('.csv')):
            data = readCsv(uploadFile)
            return render_template('table.html', tables=[data.to_html()], titles=[''])
        
        elif uploadFile.filename.lower().endswith(('.json')):
            return render_template('table.html')
        
        elif uploadFile.filename.lower().endswith(('.txt')):
            return render_template('table.html')
        
        else:
            return redirect('/')
    
    if request.method == 'POST' and request.form.get('back') == 'back':
        return redirect('/')
    
    elif request.method == 'GET':
        return redirect('/')
    
    else:
        return 'Not a valid request method for this route'
    


def readCsv(csvFileName):
    data = pd.read_csv(csvFileName, encoding='unicode_escape')

    return data

#if __name__ == '__main__':
#    checkReq()
#    app.run(debug=True)
// charts.js


// Test Function
function testPrint(data, labels){
    for (let i = 0, text = "", text1 = ""; i < data.length; i++) {
        text += data[i] + "<br>";
        text1 += labels[i] + "<br>";
    }
}

function printDataHumi(dataValue, dataLabel){
    var humiDate = dataValue
    var humiLabel = dataLabel
    //console.log(nameLabel)

    for (var i=0; i < (humiLabel.length-3); i++) {
      document.write("<td> " + humiLabel[i] + ": " + parseFloat(humiDate[i].toFixed(2)) + " &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</td>");
      //console.log(nameLabel[i])
    }
}

function printDataTemp(dataValue, dataLabel){
    var TempDate = dataValue
    var TempLabel = dataLabel
    //console.log(nameLabel)

    for (var i=3; i < TempLabel.length; i++) {
      document.write("<td> " + TempLabel[i] + ": " + parseFloat(TempDate[i].toFixed(2)) + "&nbsp&nbsp&nbsp&nbsp</td>");
      //console.log(nameLabel[i])
    }
}

// Generate Line Graphs
function createLineChart(labels, dataHumi, dataTemp, canvasName) {
    for (let i = 0; i < canvasName.length; i++) {
        //console.log(labels)
        var ctx = document.getElementById(canvasName).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature',
                    data: dataTemp,
                    fill : false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y',
                }, 
                {
                    label: 'Humidity',
                    data: dataHumi,
                    fill : false,
                    borderColor: 'rgb(192, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y1',
                }
            ]
            },
            options: {
                plugins: {
                    // Set title
                    title: {
                        font: {
                            weight: 'bold',
                            size: 20
                        },
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'left',
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        display: true,
                        position: 'right',
                
                        // grid line settings
                        grid: {
                          drawOnChartArea: false, // only want the grid lines for one axis to show up
                        },
                      },
                }
            }
        });
    }
}


// Send line graph canvas to backend
function sendLine() {
    var graphName = document.getElementById('lineName').value;
    var graph = document.getElementById('northJune');
    var graphDataURL = graph.toDataURL('image/png');
    console.log(graphDataURL)
    
    $.ajax({
        url: '/dashboard/download',
        type: 'POST',
        data: { 'graphBase64' : graphDataURL,
                'graphName' : graphName
        },
        error: function(error) {
            console.log(error)
        },
        timeout: 10000
        
    });
    console.log('done')
}


// Take screenshot of dashboard
function screenshot(){
    html2canvas(
        document.getElementById('dashboard')).then(
            function(canvas) {                
                // Convert image of dashboard into base64
                var base64URL = canvas.toDataURL('image/png');
                // var dashboard = 

                // AJAX request
               $.ajax({
                url: '/dashboard/download',
                type: 'POST',
                data: { 'graphBase64' : base64URL,
                        'graphName' : 'dashboardName'
                },
                });
            });

}
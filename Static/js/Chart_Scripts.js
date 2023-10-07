// charts.js


// Test Function
function testPrint(data, labels){
    for (let i = 0, text = "", text1 = ""; i < data.length; i++) {
        text += data[i] + "<br>";
        text1 += labels[i] + "<br>";
    }
}

function printData(month, dataValue, dataLabel){
    var myArray = dataValue
    var value = myArray[month]
    var nameLabel = dataLabel[month]
    console.log(nameLabel)

    for (var i=0; i < value.length; i++) {
      document.write("<tr> " + nameLabel[i] + ": " + parseFloat(value[i].toFixed(2)) + " </tr>");
      if (i == 2){
        document.write("</br>");
      }
      console.log(nameLabel[i])
    }
}

// Generate Line Graphs
function createLineChart(data, labels, canvasName) {
    for (let i = 0; i < data.length; i++) {
        var ctx = document.getElementById(canvasName[i]).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels[i],
                datasets: [{
                    label: 'Temperature',
                    data: data[i],
                    fill : false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    yAxisID: 'y',
                }, 
                {
                    label: 'Humidity',
                    data: data[i],
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
// charts.js



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
        console.log(canvasName)
        console.log(labels)
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
                        beginAtZero: false,
                        suggestedMin : 20,
                        type: 'linear',
                        display: true,
                        position: 'left',
                    },
                    y1: {
                        beginAtZero: false,
                        suggestedMin : 20,
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

// charts.js


// Test Function
function testPrint(data, labels){
    for (let i = 0, text = "", text1 = ""; i < data.length; i++) {
        text += data[i] + "<br>";
        text1 += labels[i] + "<br>";
    }
}

// Generate Line Graphs
function createLineChart(title, data, labels, canvasName) {
    for (let i = 0; i < data.length; i++) {
        var ctx = document.getElementById(canvasName[i]).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels[i],
                datasets: [{
                    label: 'Increase In Humidity',
                    data: data[i],
                    fill : false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                plugins: {
                    // Set title
                    title: {
                        display: true,
                        text: "",
                        align: 'center',
                        font: {
                            weight: 'bold',
                            size: 20
                        },
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// CreateBarChart
function createBarChart(title, data, labels) {
    var ctx = document.getElementById('BarChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Frequency',
                data: data,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: {
                   display: true,
                   text: title,
                   align: 'center',
                   font: {
                      weight: 'bold',
                      size: 20
                   },
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
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


function createLineChartTest(title, data, labels, canvasName) {
    for (let i = 0; i < data.length; i++) {
        var ctx = document.getElementById(canvasName[i]).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels[i],
                datasets: [{
                    label: 'Sample Increase In Humidity',
                    data: data[i],
                    fill : false,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                plugins: {
                    // Set title
                    title: {
                       display: true,
                       text: title[i],
                       align: 'center',
                       font: {
                          weight: 'bold',
                          size: 20
                       },
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    };
    var graphName = document.getElementById('lineName').value;
    var graph = document.getElementById('northJune');
    var graphDataURL = graph.toDataURL('image/png');
    console.log(graphDataURL)
    $.ajax({
        url: '/dashboard/download',
        type: 'POST',
        timeout: 3000,
        data: { 'graphBase64' : graphDataURL,
                'graphName' : graphName
        },
        error: function(error) {
            console.log(error)
        }
    });
}



function sendLineTest(graphName, graph) {
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
        }
    });
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
// charts.js

// CreateBarChart
function createBarChart(data, labels) {
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
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}



// CreateLineChart
function createLineChart(data, labels) {
    var ctx = document.getElementById('LineChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Sample Increase In Humidity',
                data: data,
                fill : false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },

    });
}



// Send bar graph canvas to backend
function sendBar() {
    var graphName = document.getElementById('barName').value;
    var graph = document.getElementById('BarChart');
    var graphDataURL = graph.toDataURL('image/png');
    //console.log(dataURL);
    //var base64 =  dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
    //var base64 = getBase64Image(document.getElementById("BarChart")); 
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


// Send line graph canvas to backend
function sendLine() {
    var graphName = document.getElementById('lineName').value;
    var graph = document.getElementById('LineChart');
    var graphDataURL = graph.toDataURL('image/png');
    //console.log(dataURL);
    //var base64 =  dataURL.replace(/^data:image\/(png|jpeg);base64,/, "");
    //var base64 = getBase64Image(document.getElementById("BarChart")); 
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
                document.body.appendChild(canvas);
                
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
                success: function(data){
                     console.log('Upload successfully');
                    }
                });
            });

}
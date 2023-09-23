// charts.js

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
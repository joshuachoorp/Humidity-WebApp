// test


// Send line graph canvas to backend
function sendLineScript() {
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
        }
    });
}


function sendLineTestScript(graphName, graph) {
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
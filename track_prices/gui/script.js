const http = new XMLHttpRequest();
const url = 'http://localhost:5003?item_model=bx80684i99900k'
http.open("GET", url)
http.responseType = "json"
http.send()


http.onreadystatechange=(e)=> {
    data = http.response
    var dates = []
    var prices = []
    data.forEach(day => {
        console.log(day['date'], day['amazon']);
        dates.push(day['date']);
        prices.push(day['amazon']);
    });
    
    var ctx = document.getElementById('retailer_chart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: dates,
            datasets: [{
                label: 'My First dataset',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: prices
            }]
        },

        // Configuration options go here
        options: {}
    });
}


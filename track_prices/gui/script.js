var USING_FAKE_DATE = true

const http = new XMLHttpRequest();

let url = 'http://localhost:5003?item_model=bx80684i99900k'

if(USING_FAKE_DATE) {
    url = 'http://localhost:5003/fake_data'
}

http.open("GET", url)
http.responseType = "json"
http.send()

http.onreadystatechange=(e)=> {
    data = http.response
    var dates = []
    var prices = []
    data.forEach(day => {
        dates.push(day['date']);
        prices.push(day['amazon']);
    });

    var max = calcMax(prices);
    var min = calcMin(prices);

    var ctx = document.getElementById('retailer_chart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            labels: dates,
            datasets: [{
                label: 'My First dataset',
                // backgroundColor: 'rgb(255, 99, 132)',
                fill: false,
                borderColor: 'rgb(201, 46, 111)',
                data: prices
            }]
        },

        // Configuration options go here
        options: {
          scales: {
            yAxes: [{
              display: true,
              ticks: {
                suggestedMin: min - 50, // The minimum y-value
                suggestedMax: max + 50 // The maximum y-value
              }
            }]
          }
        }
    });
}

function calcMax(prices) {
    var max = 0;

    prices.forEach(price => {
        if (price > max) {
            max = price;
        }
    });

    return max;
}

function calcMin(prices) {
    var min = prices[0];

    prices.forEach(price => {
        if (price < min) {
            min = price;
        }
    });

    return min;
}

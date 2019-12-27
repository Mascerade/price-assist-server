var USING_FAKE_DATE = true

const http = new XMLHttpRequest();

let url = 'http://localhost:5003?item_model=bx80684i99900k'

if(USING_FAKE_DATE) {
    url = 'http://localhost:5003/fake_data'
}

function generateChart() {
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
        var std = Math.round(calcStd(prices))

        var ctx = document.getElementById('retailer_chart').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: dates,
                datasets: [{
                    label: 'Fake Data',
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
                    suggestedMin: min - std, // The minimum y-value
                    suggestedMax: max + std // The maximum y-value
                  }
                }]
              }
            }
        });
    }
}

generateChart();

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

function calcAvg(prices) {
    var sum = 0

    prices.forEach(price => {
        sum += price;
    });

    return sum / prices.length;
}

function calcStd(prices) {
    var mean = calcAvg(prices);
    var sqSum = 0;

    prices.forEach(price => {
        sqSum += Math.pow(price - mean, 2);
    });

    return Math.sqrt(sqSum / (prices.length - 1));
}

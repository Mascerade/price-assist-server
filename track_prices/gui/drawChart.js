function generateChart(userInput) {
    console.log(userInput)
    var USING_FAKE_DATE = false;

    const http = new XMLHttpRequest();

    let url = 'http://localhost:5003?item_model=' + userInput

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

        prices.pop(prices.length - 1);
        dates.pop(data.length - 1);
        item_model = data[data.length - 1]

        var max = calcMax(prices);
        var min = calcMin(prices);
        var std = Math.round(calcStd(prices))

        var ctx = document.getElementById('retailer-chart').getContext('2d');
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: dates,
                datasets: [{
                    label: item_model,
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

function getProduct() {
    var searchButton = document.getElementById("product-search-button");
    searchButton.disabled = true;

    var searchForm = document.getElementById("user-search")
    var product = searchForm.value

    generateChart(product)

    searchButton.disabled = false;
    searchForm.value = "";
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

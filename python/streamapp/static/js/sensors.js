var actualData = {};
var myChart_1 = null;
var myChart_2 = null;

function read_table() {
    $.ajax({
        type: "GET",
        url: "/sensors?read=1",
        dataType: "json"
    })
    .done(function(data) {
        var tableHtml = '';

        actualData = Object.entries(data);
        for (const [key, value] of actualData) {
            tableHtml += `
                <tr>
                    <td>${key}</td>
                    <td>${value[0]} ${value[1]}</td>
                    <td>${value[2]}</td>
                </tr>
            `;
        }
        $("#table-sensors").html(tableHtml)
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR, textStatus, errorThrown);
    });
}

function chartjs_removeData(chart) {
    if (chart.data.labels.length > 64) {
        chart.data.labels.shift();
        chart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        chart.update();
    }
}

function chartjs_addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset, index) => {
        dataset.data.push(data[index]);
    });
    chart.update();
}

// On loading page read sensors
$(document).ready(function () {
    read_table();

    myChart_temp = new Chart("myChart_temp", {
        type: "line",
        data: {
          datasets: [{
            label: "Temp 0",
            fill: false,
            backgroundColor: "#17a2b8",
            borderColor: "#17a2b8",
          },
          {
            label: "Temp 1",
            fill: false,
            backgroundColor: "#dc3545",
            borderColor: "#dc3545",
          }]
        },
        options: {
            title: {
                display: true,
                text: 'Temperature'
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'temperature [°C]'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time'
                    }
                }]
            }
        }
    });
    myChart_humid = new Chart("myChart_humid", {
        type: "line",
        data: {
          datasets: [{
            label: "Humidity 0",
            fill: false,
            backgroundColor: "#ffc107",
            borderColor: "#ffc107",
          }]
        },
        options: {
            title: {
                display: true,
                text: 'Humidity'
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'humidity [%)]'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time'
                    }
                }]
            }
        }
    });
    myChart_press = new Chart("myChart_press", {
        type: "line",
        data: {
          datasets: [{
            label: "Pressure 0",
            fill: false,
            backgroundColor: "#198754",
            borderColor: "#198754",
          }]
        },
        options: {
            title: {
                display: true,
                text: 'Pressure'
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'pressure [hPa]'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time'
                    }
                }]
            }
        }
    });
    myChart_soil = new Chart("myChart_soil", {
        type: "line",
        data: {
            datasets: [{
                label: "Soil 0",
                fill: false,
                backgroundColor: "#17a2b8",
                borderColor: "#17a2b8",
              },
              {
                label: "Soil 0",
                fill: false,
                backgroundColor: "#dc3545",
                borderColor: "#dc3545",
              }]
        },
        options: {
            title: {
                display: true,
                text: 'Soil moisture'
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'soil moisture [%]'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time'
                    }
                }]
            }
        }
    });
});

// Periodicaly update table
setInterval(() => {
    read_table();

    chartjs_removeData(myChart_temp);
    chartjs_removeData(myChart_humid);
    chartjs_removeData(myChart_press);
    chartjs_removeData(myChart_soil);

    var today = new Date();
    chartjs_addData(myChart_temp, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[0][1][0], actualData[1][1][0]]);
    chartjs_addData(myChart_humid, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[3][1][0]]);
    chartjs_addData(myChart_press, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[4][1][0]]);
    chartjs_addData(myChart_soil, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[5][1][0], actualData[6][1][0]]);
}, refreshInterval);

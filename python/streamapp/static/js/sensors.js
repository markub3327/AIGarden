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
}}

function chartjs_addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

// On loading page read sensors
$(document).ready(function () {
    read_table();

    myChart_1 = new Chart("myChart_1", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(0,80,120,1)",
            borderColor: "rgba(0,0,120,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Temp 0'
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
    myChart_2 = new Chart("myChart_2", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(120,80,0,1)",
            borderColor: "rgba(120,0,0,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Temp 1'
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
    myChart_3 = new Chart("myChart_3", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(120,80,0,1)",
            borderColor: "rgba(120,0,0,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Humidity 0'
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
    myChart_4 = new Chart("myChart_4", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(120,80,0,1)",
            borderColor: "rgba(120,0,0,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Pressure 0'
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
    myChart_5 = new Chart("myChart_5", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(120,80,0,1)",
            borderColor: "rgba(120,0,0,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Soil moisture 0'
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
    myChart_6 = new Chart("myChart_6", {
        type: "line",
        data: {
          datasets: [{
            fill: false,
            backgroundColor: "rgba(120,80,0,1)",
            borderColor: "rgba(120,0,0,0.5)",
          }]
        },
        options: {
            legend: false,
            title: {
                display: true,
                text: 'Soil moisture 1'
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


    chartjs_removeData(myChart_1);
    chartjs_removeData(myChart_2);
    chartjs_removeData(myChart_3);
    chartjs_removeData(myChart_4);
    chartjs_removeData(myChart_5);
    chartjs_removeData(myChart_6);

    var today = new Date();
    chartjs_addData(myChart_1, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[0][1][0]);
    chartjs_addData(myChart_2, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[1][1][0]);
    chartjs_addData(myChart_3, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[2][1][0]);
    chartjs_addData(myChart_4, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[3][1][0]);
    chartjs_addData(myChart_5, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[4][1][0]);
    chartjs_addData(myChart_6, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[5][1][0]);
}, refresh_interval);

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
        let tbody = document.getElementById("table-sensor");
        tbody.innerHTML = '';

        actualData = Object.entries(data);
        for (const [key, value] of actualData) {
            tbody.innerHTML += `
                <tr>
                    <td>${key}</td>
                    <td>${value[0]} ${value[1]}</td>
                    <td>${value[2]}</td>
                </tr>
            `;
        }
        
        // Firstly clean the graph 
        chartjs_removeData(myChart_temp);
        chartjs_removeData(myChart_humid);
        chartjs_removeData(myChart_press);
        chartjs_removeData(myChart_soil);

        // Store new measurements
        var today = new Date();
        chartjs_addData(myChart_temp, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[0][1][0], actualData[1][1][0]]);
        chartjs_addData(myChart_humid, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[3][1][0]]);
        chartjs_addData(myChart_press, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[4][1][0]]);
        chartjs_addData(myChart_soil, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), [actualData[5][1][0], actualData[6][1][0]]);
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
                text: 'Temperature',
                fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
            },
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                }
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'temperature [°C]',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
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
                text: 'Humidity',
                fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
            },
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                }
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'humidity [%]',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
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
                text: 'Pressure',
                fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
            },
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                }
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'pressure [hPa]',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
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
                text: 'Soil moisture',
                fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
            },
            legend: {
                display: true,
                labels: {
                    fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                }
            },
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'soil moisture [%]',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'time',
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    },
                    ticks: {
                        fontFamily: "'Poppins', 'Roboto', 'Helvetica', 'Arial', sans-serif",
                    }
                }]
            }
        }
    });

    // Get data into graphs and table
    read_table();
});

// Periodicaly update table
setInterval(() => read_table(), refreshInterval * 1000);  // in milliseconds

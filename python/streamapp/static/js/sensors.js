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
    if (chart.data.labels.length > 128) {
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
});

// Periodicaly update table
setInterval(() => {
    read_table();

    var today = new Date();

    chartjs_removeData(myChart_1);
    chartjs_removeData(myChart_2);
    chartjs_addData(myChart_1, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[0][1][0]);
    chartjs_addData(myChart_2, today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds(), actualData[1][1][0]);
}, refresh_interval);


function read_table() {
    $.ajax({
        type: "GET",
        url: "/sensors?read=1",
        dataType: "json"
    })
    .done(function(data) {
        var tableHtml = '';
        for (const [key, value] of Object.entries(data)) {
            tableHtml += `
                <tr>
                    <td>${key}</td>
                    <td>${value}</td>
                </tr>
            `;
        }
        $("#table-sensors").html(tableHtml)
    }).fail(function(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR, textStatus, errorThrown);
    });
}

// On loading page read sensors
$(document).ready(function () {
    read_table();
});

// Periodicaly update table
setInterval(read_table, refresh_interval);

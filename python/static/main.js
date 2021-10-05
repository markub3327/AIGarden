setInterval(function () {
    $.ajax({
        type: "GET",
        url: "{{ url_for('sensors') }}",
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
}, 1000);

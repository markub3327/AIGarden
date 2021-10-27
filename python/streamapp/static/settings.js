var activeRow = [];
var delTimes = [];
var newTimes = [];

function click_table(obj) {
    if (!activeRow.includes(obj))
    {
        $(obj).addClass('table-active');
        $("#removeButton").removeClass('disabled');
        activeRow.push(obj);
    }
    else
    {
        $(obj).removeClass('table-active');
        activeRow.splice(
            activeRow.indexOf(obj),
            1
        );
        if (activeRow.length < 1)
            $("#removeButton").addClass('disabled');
    }
}

function delete_time() {
    if (activeRow.length > 0)
    {
        for (let i = 0; i < activeRow.length; i++)
        {
            delTimes.push(activeRow[i].innerText);
            document.getElementById("timeTable").deleteRow(activeRow[i].rowIndex);
            $("#removeButton").blur();   // Release button
            $("#removeButton").addClass('disabled');
        }
        activeRow = []
    }
}

function add_time() {
    row = document.getElementById("timeTable").insertRow(-1);
    row.innerHTML = `
    <tr>
        <td>
            <input pattern="([0-1]?[0-9]|2[0-3]):[0-5][0-9]" type="text" class="timeInput">
        </td>
    </tr>
    `;
    row.setAttribute("onclick", "click_table(this);");
}

function save_settings(e) {
    let values = {};

    values['mode'] = document.getElementById("modeSelect").value;
    values['refresh_interval'] = document.getElementById("intervalInput").value;

    let rows = document.getElementsByClassName("timeInput");
    for (let i = 0; i < rows.length; i++)
    {
        newTimes.push(rows[i].value);
    }
    values['new_watering_schedule'] = newTimes;
    values['del_watering_schedule'] = delTimes;

    e.preventDefault();         // enable AJAX
    $.ajax({
        type: "POST",
        url: "/settings",
        data: JSON.stringify(values),
        success: function () {
            console.log("POST is successful");
            
            // refresh page
            window.location.reload();
        },
        error: function(errMsg) {
            console.log(errMsg.status);
        }
    });
}

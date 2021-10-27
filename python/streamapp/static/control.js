function control_pump(obj, id, val=null) {
    let values = {};
    let textInputs = document.getElementsByClassName('pump-value');
        
    if (val == null)
        values['pump-' + id] = textInputs[id].value;
    else
        values['pump-' + id] = val;

    // Release button
    obj.blur();

    // Display message
    document.getElementById('msgResult').innerHTML = "Pump " + id + " is set to " + values['pump-' + id] + " %";

    $.ajax({
        type: "POST",
        url: "/control",
        data: JSON.stringify(values),
        success: function () {
            console.log("POST is successful");
        },
        error: function(errMsg) {
            console.log(errMsg.status);
        }
    });
}
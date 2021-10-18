function control_pump(obj, id, val=null) {
    let values = {};
    let textInputs = document.getElementsByClassName('pump-value');

    for (i = 0; i < textInputs.length; i++)
    {
        if (i == id)
        {
            if (val == null)
                values['pump-' + i] = textInputs[id].value;
            else
                values['pump-' + i] = val;
        }
        else
            values['pump-' + i] = null; 
    }

    // Release button
    obj.blur();

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
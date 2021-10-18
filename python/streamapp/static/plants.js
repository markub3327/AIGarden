// On loading page read sensors
$(document).ready(function() {
    $("#table-plants").html(
        `
        <tr>
            <td>Amy</td>
            <td>paprika</td>
            <td>10.6.2021</td>
        </tr>
        <tr>
            <td>Deon</td>
            <td>salat</td>
            <td>1.4.2021</td>
        </tr>
        `
    );

    $("#table-desc").html(
        `
        <tr>
            <td>paprika</td>
            <td>3</td>
            <td>plodova</td>
        </tr>
        <tr>
            <td>salat</td>
            <td>1</td>
            <td>listova</td>
        </tr>
        `
    );
});
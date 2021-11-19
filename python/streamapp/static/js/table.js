class LiveTable
{
    constructor(tableId, add_id, remove_id) {
        this.activeRow = [];
        this.delRows = [];

        this.tableId = tableId;
        this.add_id = add_id;
        this.remove_id = remove_id;
    }

    click(e) {
        let obj = e.target
        let parrent = obj.parentNode
    
        // exclude by class
        if (obj.tagName.toLowerCase() != "input")
        {
            if (!this.activeRow.includes(parrent))
            {
                parrent.classList.add('table-active');
                document.getElementById(this.remove_id).classList.remove('disabled');
                this.activeRow.push(parrent);
            }
            else
            {
                parrent.classList.remove('table-active');
                this.activeRow.splice(
                    this.activeRow.indexOf(parrent),
                    1
                );
                if (this.activeRow.length < 1)
                    document.getElementById(this.remove_id).classList.add('disabled');
            }
        }
    }

    delRow(e) {
        if (this.activeRow.length > 0)
        {
            for (let i = 0; i < this.activeRow.length; i++)
            {
                // iba nove riadky neobsahuju atribut "data-id"
                if (this.activeRow[i].hasAttribute("data-id"))
                {
                    let id = this.activeRow[i].getAttribute("data-id");
                    this.delRows.push(id);
                }

                document.getElementById(this.tableId).deleteRow(this.activeRow[i].rowIndex);
                //$("#removeButton").blur();   // Release button
                document.getElementById(this.remove_id).classList.add('disabled');
            }
            this.activeRow = []
        }
    }

    addRow(e, inputParams) {
        let table = document.getElementById(this.tableId)
        let tbody = table.getElementsByTagName('tbody')[0];
        let row = tbody.insertRow();

        row.innerHTML = '';
        for (let i = 0; i < inputParams['type'].length; i++) {
            let req = "";
            if (inputParams['required'][i] == '1')
                req = "required";
    
            switch (inputParams['type'][i]) {
                case "str":
                    row.innerHTML += `
                        <td>
                            <input type="text" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "int":
                    row.innerHTML += `
                        <td>
                            <input type="number" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "time":
                    row.innerHTML += `
                        <td>
                            <input pattern="([0-1]?[0-9]|2[0-3]):[0-5][0-9]" type="text" placeholder="hh:mm" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "date":
                    row.innerHTML += `
                        <td>
                            <input pattern="([1-9]|0[1-9]|[1-2][0-9]|3[0-1])(\\.)(([1-9]|0[1-9])|(1[0-2]))(\\.)\\d{4}" type="text" placeholder="dd.mm.yyyy" style="text-align:center; max-width:100px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "range":
                    row.innerHTML += `
                        <td>
                            <input type="text" style="text-align:center; max-width:75px;" ${req}>
                            -
                            <input type="text" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "range_month":
                    row.innerHTML += `
                        <td>
                            <input pattern="(([1-9]|0[1-9])|(1[0-2]))" type="text" placeholder="mm" style="text-align:center; max-width:75px;" ${req}>
                            -
                            <input pattern="(([1-9]|0[1-9])|(1[0-2]))" type="text" placeholder="mm" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;
                case "range_time":
                    row.innerHTML += `
                        <td>
                            <input pattern="([0-1]?[0-9]|2[0-3]):[0-5][0-9]" type="text" placeholder="hh:mm" style="text-align:center; max-width:75px;" ${req}>
                            -
                            <input pattern="([0-1]?[0-9]|2[0-3]):[0-5][0-9]" type="text" placeholder="hh:mm" style="text-align:center; max-width:75px;" ${req}>
                        </td>\n
                    `;
                    break;    
            }
        }
        row.setAttribute("onclick", this.tableId+".click(event)");
    }

    getRows() {
        let table = document.getElementById(this.tableId);
        let newRows = [];
    
        for (const row of table.rows) {
            let newCells = [];
            for (const cell of row.cells) {
                // iba nove riadky obsahuju tag "input"
                content = cell.getElementsByTagName("input");
                
                // ak stlpec obsahuje niekolko vstupov sprav z nich list
                if (content.length > 1) {
                    let items = [];
                    for (let i = 0; i < content.length; i++) {
                        items.push(content[i].value);
                        //console.log("content["  + i + "]: " + content[i].value);
                    }
                    newCells.push(items);
                }
                // ak ide o jeden vstup na stlpec
                else if (content.length == 1) {
                    newCells.push(content[0].value);
                }
            }
            // ak neexistuje ziaden stlpec v aktualnom riadku vynechaj ho vo vystupe
            if (newCells.length > 0)
                newRows.push(newCells);
        }
    
        return newRows;
    }
}
class LiveTable
{
    constructor(tableId, add_id, remove_id, input_fields) {
        this.input_fields = input_fields;
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
                let remove_btn = document.getElementById(this.remove_id);
                remove_btn.blur();   // Release button
                document.getElementById(this.remove_id).classList.add('disabled');
            }
            this.activeRow = []
        }
    }

    addRow(e) {
        let table = document.getElementById(this.tableId)
        let tbody = table.getElementsByTagName('tbody')[0];
        let row = tbody.insertRow();

        row.innerHTML = '';
        for (let i = 0; i < this.input_fields.length; i++) {    
            switch (this.input_fields[i].type) {
                case "range_number":
                    row.innerHTML += `
                        <td>
                            <input class="text-center col-12" type="number" ${this.input_fields[i].attribute}>
                            -
                            <input class="text-center col-12" type="number" ${this.input_fields[i].attribute}>
                        </td>\n
                    `;
                    break;
                case "range_month":
                    row.innerHTML += `
                        <td>
                            <input pattern="(([1-9]|0[1-9])|(1[0-2]))" class="text-center col-12" type="number" placeholder="mm" ${this.input_fields[i].attribute}>
                            -
                            <input pattern="(([1-9]|0[1-9])|(1[0-2]))" class="text-center col-12" type="number" placeholder="mm" ${this.input_fields[i].attribute}>
                        </td>\n
                    `;
                    break;
                default:
                    row.innerHTML += `
                        <td>
                            <input class="text-center col-12" type="${this.input_fields[i].type}" ${this.input_fields[i].attribute}>
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
                let content = cell.getElementsByTagName("input");

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
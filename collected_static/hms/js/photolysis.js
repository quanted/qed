var valid_wavelengths = [280.0, 282.5, 285.0, 287.5, 290.0, 292.5, 295.0,
    297.5, 300.0, 302.5, 305.0, 307.5, 310.0, 312.5,
    315.0, 317.5, 320.0, 323.1, 330.0, 340.0, 350.0,
    360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0,
    430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0,
    500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0,
    675.0, 700.0, 750.0, 800.0];
var current_wavelengths = [];
var available_wavelengths = [];

$(document).ready(function () {

    // form initialization
    initializeInputForm();

    // form events
    $('#id_typical_ephemeride_values').change(toggleEphemerideOptions);
    $('#id_contaminant_type').change(toggleContainmentType);
    $('#input_form').click(setInputForm);
    $('#json_form').click(setJsonInput);
    $('#id_json_input').on("blur", formatJson);
    $('.wavelengthTable').on("click", "td", editTableCell);
    $('.remove_button').click(removeTableRow);
    $('#add_button').click(addToTable);
});

function formatJson() {
    try {
        JSON.parse($('#id_json_input').val());
        $('#error_p').html("");
    }
    catch (e) {
        $('#error_p').html("Error: Invalid json string." + e.message);
    }
}

function setInputForm() {
    $('#input_table tr').each(function (i, row) {
        if (!row.children[0].innerText.includes("Json Input")) {
            $(row).removeClass("hidden");
        }
        else {
            $(row).addClass("hidden");
        }
    });
    toggleEphemerideOptions();
    $('#inputOptions').attr('action', "/hms/water_quality/photolysis/output")
}

function setJsonInput() {
    $('#input_table tr').each(function (i, row) {
        // var name = row.children[0].innerText;
        if (!row.children[0].innerText.includes("Input")) {
            $(row).addClass("hidden");
        }
    });
    var json_input = $('.json_input_data');
    json_input.closest('tr').removeClass('hidden');
    $('#inputOptions').attr('action', "/hms/water_quality/photolysis/output/json")
}

function initializeInputForm() {
    $('.json_input_data').closest('tr').addClass("hidden");
    $('#id_latitude').closest('tr').addClass("hidden");
    $('#id_solar_declination_0').closest('tr').addClass("hidden");
    $('#id_right_ascension_0').closest('tr').addClass("hidden");
    $('#id_sidereal_time_0').closest('tr').addClass("hidden");
    setInitialWavelengthTable();
    removeRequiredFromForm();

    var addButton = document.createElement('button');
    addButton.id = 'add_button';
    addButton.title = "Add new wavelength and coefficients";
    addButton.innerHTML = "+";

    $('#id_wavelength_table').closest("td")[0].appendChild(addButton);
}

function toggleEphemerideOptions() {
    var state = $('#id_typical_ephemeride_values').val();
    hideEphemerideOptions(false);
    if (state === "yes") {
        $("input.ephemeride_0").map(function () {
            $(this).closest('tr').addClass("hidden");
        });
    }
    else {
        $("input.ephemeride_1").map(function () {
            $(this).closest('tr').addClass("hidden");
        });
    }
}

function hideEphemerideOptions(hide) {
    if (hide === false) {
        $("input.ephemeride_0").map(function () {
            $(this).closest('tr').removeClass("hidden");
        });
        $("input.ephemeride_1").map(function () {
            $(this).closest('tr').removeClass("hidden");
        });
    }
    else {
        $("input.ephemeride_0").map(function () {
            $(this).closest('tr').addClass("hidden");
        });
        $("input.ephemeride_1").map(function () {
            $(this).closest('tr').addClass("hidden");
        });
    }
}

function toggleContainmentType() {
    var type = $('#id_contaminant_type').val();
    if (type === "biological") {
        // $('.wlCol3')[0].innerHTML = "Biological Weighting Function (hr**(-1)Watts**(-1)cm**2 nm)";
        $('.wlCol3')[0].innerHTML = "Biological Absorption Coefficients (L/(mole cm))";
    }
    else {
        $('.wlCol3')[0].innerHTML = "Chemical Absorption Coefficients (L/(mole cm))";
    }
    $('#id_wavelength_table').val(tableToDict($('#wlTable tr')));
}

function setInitialWavelengthTable() {
    var initialTable = document.createElement("TABLE");
    $(initialTable).addClass("wavelengthTable");
    initialTable.id = 'wlTable';

    // Set initial values
    var wavelengthData = [
        ["297.50", "0.069000", "11.100000"],
        ["300.00", "0.061000", "4.670000"],
        ["302.50", "0.057000", "1.900000"],
        ["305.00", "0.053000", "1.100000"],
        ["307.50", "0.049000", "0.800000"],
        ["310.00", "0.045000", "0.530000"],
        ["312.50", "0.043000", "0.330000"],
        ["315.00", "0.041000", "0.270000"],
        ["317.50", "0.039000", "0.160000"],
        ["320.00", "0.037000", "0.100000"],
        ["323.10", "0.035000", "0.060000"],
        ["330.00", "0.029000", "0.020000"]];
    setTableRows(initialTable, wavelengthData);

    // Set table headers
    var header = initialTable.createTHead();
    var hRow = header.insertRow(0);
    var hWL = hRow.insertCell(0);
    hWL.innerHTML = "Wavelength (nm)";
    $(hWL).addClass("wlTableHeader wlCol1");
    var wAC = hRow.insertCell(1);
    wAC.innerHTML = "Water Attenuation Coefficients (m**-1)";
    $(wAC).addClass("wlTableHeader wlCol2");
    var aC = hRow.insertCell(2);
    aC.innerHTML = "Chemical Absorption Coefficients (L/(mole cm))";
    $(aC).addClass("wlTableHeader wlCol3");

    var inputTable = $('#id_wavelength_table').closest("td")[0];
    inputTable.appendChild(initialTable);
    current_wavelengths.push(297.50, 300.00, 302.50, 305.00, 307.50, 310.00, 312.50, 315.00, 317.50, 320.00, 323.10, 330.00);
    available_wavelengths.push(280.0, 282.5, 285.0, 287.5, 290.0, 292.5, 295.0, 340.0, 350.0,
        360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0,
        500.0, 525.0, 550.0, 575.0, 600.0, 625.0, 650.0, 675.0, 700.0, 750.0, 800.0);

    $('#id_wavelength_table').val(tableToDict($('#wlTable tr')));
}

function setTableRows(table, values) {
    values.map(function (iv, i) {
        var row = table.insertRow(i);
        iv.map(function (jv, j) {
            var cell = row.insertCell(j);
            cell.innerHTML = jv;
        });
        var removeBtn = document.createElement('button');
        $(removeBtn).addClass('remove_button');
        removeBtn.title = "Remove row from table";
        removeBtn.innerHTML = "-";
        var rmBtn = row.insertCell(-1);
        rmBtn.appendChild(removeBtn);
    });
}

function editTableCell() {
    if ((this.cellIndex > 0 && this.cellIndex < 3) && this.childElementCount === 0) {
        var value = this.innerHTML;
        this.innerHTML = '<input id="wlTblEdit" type="text" onblur="setTableCellValue()" value="' + value + '">';
        document.getElementById("wlTblEdit").focus();
    }
}

function setTableCellValue() {
    var value = $('#wlTblEdit').val();
    if ($.isNumeric(value)) {
        $('#wlTblEdit').closest('td')[0].innerHTML = value;
        $('#error_p').html("");
    }
    else {
        $('#error_p').html("Error: Non-numeric value provided.");
    }
    $('#id_wavelength_table').val(tableToDict($('#wlTable tr')));
}

function removeTableRow() {
    var table = document.getElementById("wlTable");
    if (table.childNodes[1].childElementCount > 1) {
        var cWL = parseFloat(this.closest('tr').childNodes[0].innerHTML);
        table.deleteRow(this.closest('tr').rowIndex);
        addRemoveWL(false, cWL);
    }
    $('#id_wavelength_table').val(tableToDict($('#wlTable tr')));
}

function addToTable() {
    if ($('#id_wavelength_table').closest("td")[0].childElementCount <= 3) {
        var addWl = '<label for="selected_wavelength">Wavelength</label><select name="wavelengths" id="selected_wavelength">';
        available_wavelengths.map(function (wl) {
            addWl += '<option value="' + wl + '">' + wl + '</option>';
        });
        addWl += '</select><button type="button" id="add_wavelength" onclick="addWLToTable()">Add</button>';
        var wlInputSelection = document.createElement('div');
        wlInputSelection.innerHTML = addWl;
        $(wlInputSelection).addClass("addWavelengthSelect");
        $('#id_wavelength_table').closest("td")[0].appendChild(wlInputSelection);
    }
    return false;
}

function addWLToTable() {
    var value = $('#selected_wavelength').val();
    var table = document.getElementById("wlTable");
    var nRow = table.insertRow(-1);
    var c1 = nRow.insertCell(0);
    c1.innerHTML = value;
    var c2 = nRow.insertCell(1);
    c2.innerHTML = "0.000";
    var c3 = nRow.insertCell(2);
    c3.innerHTML = "0.000";
    var removeBtn = document.createElement('button');
    $(removeBtn).addClass('remove_button');
    removeBtn.title = "Remove row from table";
    removeBtn.innerHTML = "-";
    var rmBtn = nRow.insertCell(-1);
    rmBtn.appendChild(removeBtn);
    addRemoveWL(true, value);

    $('#id_wavelength_table').closest("td")[0].removeChild(document.getElementsByClassName('addWavelengthSelect')[0]);
    $('#id_wavelength_table').val(tableToDict($('#wlTable tr')));
    return false;
}

function removeRequiredFromForm() {
    $(document.getElementById('inputOptions').elements).map(function (i, ele) {
        ele.required = false;
    });
}

function addRemoveWL(add, wl) {
    wl = parseFloat(wl);
    if (add === true) {
        available_wavelengths.splice(available_wavelengths.indexOf(wl), 1);
        current_wavelengths.push(wl);
        current_wavelengths.sort();
        available_wavelengths.sort();
    }
    else{
        current_wavelengths.splice(current_wavelengths.indexOf(wl), 1);
        available_wavelengths.push(wl);
        current_wavelengths.sort();
        available_wavelengths.sort();
    }
}

function tableToDict(tableRows){
    var array = [];
    tableRows.each(function(){
        var rowArray = [];
        var rowData = $(this).find('td');
        rowData.each(function(){
            rowArray.push($(this).text());
        });
        array.push(rowArray);
    });
    return JSON.stringify(array);
}
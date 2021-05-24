// var baseUrl = "/hms/rest/api/meteorology/solar/";
var baseUrl = "/hms/rest/api/v3/meteorology/solar/";

var dataTable;
var columnsDict = {};
var columns;

$(document).ready(function () {

    $('#overview_block').accordion({
        collapsible: true,
        heightStyle: "content"
    });

    $('#id_date').parent().parent().hide();

    $('#id_model').change(function () {
        if (this.value === "day") {
            $("#id_local_time").parent().parent().hide();
            $("#id_year").parent().parent().hide();
            $("#id_date").parent().parent().show();
        }
        else {
            $("#id_local_time").parent().parent().show();
            $("#id_year").parent().parent().show();
            $('#id_date').parent().parent().hide();
        }
    });

    $('#id_model').trigger("change");

    $('#id_area_of_interest').on('change', updateAoISelection);

    setTimeout(setOverviewTabindex, 100);
    setTimeout(updateAoISelection, 100);
});

function setOutputUI(){
    columns = componentData.metadata.columns.split(", ");
    setMetadata();
    setOutputPage();
    setDataTable();
    // drawInitialPlot();
    var xAxis = dataTable.getNumberOfColumns() - 4;
    var yAxis = [dataTable.getNumberOfColumns() - 1];
    drawPlot(xAxis, yAxis);
    setTimeout(setPlotSelection, 300);
    document.getElementById('updatePlot').addEventListener("click", updatePlot);
}

function getParameters(){
    // Dataset specific request object

    var requestJson = {
        "model": $('#id_model').val(),
        "localTime": $('#id_local_time').val(),
        "dateTimeSpan": {
            "startDate": $('#id_date').val(),
            // "dateTimeFormat": $("#id_datetimeformat").val()
        },
        "geometry": {
            "point": {
                "latitude": $("#id_latitude").val(),
                "longitude": $("#id_longitude").val()
            },
            "timezone": {
                "offset": $('#id_timezone').val()
            }
        },
        "dataValueFormat": $("#id_outputformat").val(),
        "units": "default",
        "outputFormat": "json"
    };
    if ($('#id_model').val() === "year"){
        requestJson['localTime'] = $('#id_local_time').val();
        var inputDate = new Date($('#id_date').val());
        var startDate = new Date(inputDate.setDate(inputDate.getDate()));
        var endDate = new Date(inputDate.setDate(inputDate.getDate() + 365));
        requestJson['dateTimeSpan']['startDate'] = startDate.toISOString();
        requestJson['dateTimeSpan']['endDate'] = endDate.toISOString();
    }
    else{
        var inputDate = new Date($('#id_date').val());
        var startDate = new Date(inputDate.setDate(inputDate.getDate()));
        var endDate = new Date(inputDate.setDate(inputDate.getDate() + 1));
        requestJson['dateTimeSpan']['startDate'] = startDate.toISOString();
        requestJson['dateTimeSpan']['endDate'] = endDate.toISOString();
    }
    if($('#id_area_of_interest').val() === "Catchment Centroid"){
        delete requestJson["geometry"]["point"];
        requestJson["geometry"]["comid"] = $("#id_catchment_comid").val()
    }
    return requestJson;
}

function setOutputPage(){
    var outputTablesHTML = "<div id='plots' class='pane-content'><h3>Solar Calculator Charts</h3>" +
        "<div id='lineChartDiv'></div><div id='chartForm'><form id='setChartAxies'>" +
        "<label for='x-Axis'>X-Axis:</label><select id='x-Axis'></select>" +
        "<label for='y-Axis'>Y-Axis:</label><select multiple id='y-Axis'></select>" +
        "<button type='button' id='updatePlot'>Update Plot</button></form></div></div>" +
        "<div id='dataTableDiv' class='display table-style'><div id='output_graph_1'></div></div>";
    $('#output_data').html(outputTablesHTML);
}

function setDataTable() {
    dataTable = new google.visualization.DataTable();
    // Set Date/Time column based on requested submodel
    if ((componentData.dataset).includes("Year")) {
        dataTable.addColumn('date', 'Date', 'MM-DD-YYYY');
        dataTable.addColumn('timeofday', 'Time');
    }
    else {
        dataTable.addColumn('datetime', 'Date', 'MM-DD-YYYY HH:mm:SS');
    }

    columns.map(function (i) {
        if (!(i.includes("Time (hrs past local midnight)"))) {
            if (i.includes("(LST)")) {
                dataTable.addColumn('timeofday', i);
            }
            else {
                dataTable.addColumn('number', i);
            }
        }
    });

    $.each(componentData['data'], function (index, row) {
        var r = [];
        if ((componentData.dataset).includes("Year")) {
            var d = index.split('/');
            r.push(new Date(d[2], d[0] - 1, d[1]));
        }
        else {
            var dt = index.split(' ');
            var d = dt[0].split('/');
            var t = dt[1].split(':');
            r.push(new Date(d[2], d[0] - 1, d[1], t[0], t[1], t[2]));
        }
        $.each(row, function (key, value) {
            if (!value.includes(":")) {
                r.push(parseFloat(value));
            }
            else {
                var t = value.split(':');
                var time = [parseInt(t[0]), parseInt(t[1]), parseInt(t[2])];
                r.push(time);
            }
        });
        dataTable.addRow(r);
    });
    var vFormatter = new google.visualization.NumberFormat(
        {fractionDigits: 8}
    );

    // Format based on dataset
    if ((componentData.dataset).includes("Year")) {
        var c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29];
        $(c).map(function (i) {
            vFormatter.format(dataTable, i);
        });
    }
    else {
        var c = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28];
        $(c).map(function (i) {
            vFormatter.format(dataTable, i);
        });
    }
    dataTable.setProperty(0, 0, {style: 'width:100px'});
    var table = new google.visualization.Table(document.getElementById('output_graph_1'));
    table.draw(dataTable, {allowHtml: true, showRowNumber: false, width: '100%', height: '100%', page: 'enable'});
}

function drawInitialPlot() {
    var columnIndex = [dataTable.getNumberOfColumns() - 4, dataTable.getNumberOfColumns() - 1];
    var plotData = new google.visualization.DataTable();
    plotData.addColumn(dataTable.getColumnType(columnIndex[0]), dataTable.getColumnLabel(columnIndex[0]));
    plotData.addColumn(dataTable.getColumnType(columnIndex[1]), dataTable.getColumnLabel(columnIndex[1]));
    var rowIndex = [];
    for (var i = 0; i < dataTable.getNumberOfRows(); i++) {
        rowIndex.push(i);
    }
    rowIndex.map(function (r) {
        var row = [];
        columnIndex.map(function (c) {
            row.push(dataTable.getValue(r, c));
        });
        plotData.addRow(row);
    });
    var chartOptions = {
        title: 'Solar Calculator Graph',
        legend: {position: 'right'}
    };
    var lineChart = new google.visualization.LineChart(document.getElementById('lineChartDiv'));
    lineChart.draw(plotData, chartOptions);
    setTimeout(setPlotSelection, 300);
}

function setPlotSelection() {
    var selection = [];
    for (var i = 0; i < dataTable.getNumberOfColumns(); i++) {
        columnsDict[dataTable.getColumnLabel(i)] = i;
        selection.push(dataTable.getColumnLabel(i));
    }
    var xAxis = document.getElementById('x-Axis');
    var yAxis = document.getElementById('y-Axis');
    for (var j = 0; j < selection.length; j++) {
        var opX = document.createElement('option');
        opX.innerHTML = selection[j];
        opX.value = j;
        xAxis.appendChild(opX);
        var opY = document.createElement('option');
        opY.innerHTML = selection[j];
        opY.value = j;
        yAxis.appendChild(opY);
    }
}

function updatePlot(){
    var xAxis = parseInt(document.getElementById('x-Axis').value);
    var yAxis = $('#y-Axis').val();
    drawPlot(xAxis, yAxis);
    return false;
}

function drawPlot(xAxis, yAxis) {
    // var xAxis = parseInt(document.getElementById('x-Axis').value);
    // var yAxis = $('#y-Axis').val();
    var columnIndex = [xAxis];
    yAxis.map(function (y) {
        columnIndex.push(parseInt(y));
    });
    var plotData = new google.visualization.DataTable();
    columnIndex.map(function (cI) {
        var type = dataTable.getColumnType(cI);
        var label = dataTable.getColumnLabel(cI);
        plotData.addColumn(type, label);
    });
    var rowIndex = [];
    for (var i = 0; i < dataTable.getNumberOfRows(); i++) {
        rowIndex.push(i);
    }
    rowIndex.map(function (r) {
        var row = [];
        columnIndex.map(function (c) {
            row.push(dataTable.getValue(r, c));
        });
        plotData.addRow(row);
    });
    var chartOptions = {
        title: 'Solar Calculator Graph',
        legend: {position: 'right'}
    };
    var lineChart = new google.visualization.LineChart(document.getElementById('lineChartDiv'));
    lineChart.draw(plotData, chartOptions);
    return false;
}


function updateAoISelection(){
    var source = $("#id_source").val();
    if(source === "ncei"){
        $("#id_area_of_interest").parent().parent().hide();
        $("#id_latitude").parent().parent().hide();
        $("#id_longitude").parent().parent().hide();
        $("#id_catchment_comid").parent().parent().hide();
    }
    else {
        $("#id_area_of_interest").parent().parent().show();
        var aoi = $('#id_area_of_interest').val();
        if (aoi === "Latitude/Longitude") {
            $("#id_latitude").parent().parent().show();
            $("#id_longitude").parent().parent().show();
            $("#id_catchment_comid").parent().parent().hide();
        } else {
            $("#id_latitude").parent().parent().hide();
            $("#id_longitude").parent().parent().hide();
            $("#id_catchment_comid").parent().parent().show();
        }
    }
}

function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}
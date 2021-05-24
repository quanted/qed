google.charts.load('current', {'packages': ['table', 'corechart']});
google.charts.setOnLoadCallback(setDataTable);
google.charts.setOnLoadCallback(setMetaTable);
google.charts.setOnLoadCallback(drawInitialPlot);

var dataTable;
var columnsDict = {};

function setDataTable() {
    dataTable = new google.visualization.DataTable();
    // Set Date/Time column based on requested submodel
    if ((data.dataset).includes("Year")) {
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

    $.each(data['data'], function (index, row) {
        var r = [];
        if ((data.dataset).includes("Year")) {
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
                var test = parseFloat(value);
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
    if ((data.dataset).includes("Year")) {
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
    var table = new google.visualization.Table(document.getElementById('test-graph-1'));
    table.draw(dataTable, {allowHtml: true, showRowNumber: false, width: '100%', height: '100%', page: 'enable'});
}

function setMetaTable() {
    var metaTable = new google.visualization.DataTable();
    metaTable.addColumn('string', 'MetaData');
    metaTable.addColumn('string', 'Value');
    $.each(data['metadata'], function (key, value) {
        metaTable.addRow([key, value]);
    });
    var table = new google.visualization.Table(document.getElementById('test-graph-2'));
    table.draw(metaTable, {allowHtml: true, showRowNumber: false, width: '100%', height: '100%', page: 'enable'});
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
        // curveType: 'function',
        vAxes: {
            1: {title: dataTable.getColumnLabel(columnIndex[0])},
            0: {title: dataTable.getColumnLabel(columnIndex[1])}
        },
        legend: {position: 'bottom'}
    };
    var lineChart = new google.visualization.LineChart(document.getElementById('lineChartDiv'));
    lineChart.draw(plotData, chartOptions);
    setTimeout(setPlotSelection, 300);
}

function setAccordions() {
    $('#content').accordion({
        collapsible: true,
        heightStyle: "content",
    });
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

function updatePlot() {
    var xAxis = parseInt(document.getElementById('x-Axis').value);
    var yAxis = $('#y-Axis').val();
    var columnIndex = [xAxis];
    yAxis.map(function (y) {
        columnIndex.push(parseInt(y));
    });
    var plotData = new google.visualization.DataTable();
    columnIndex.map(function (cI) {
        plotData.addColumn(dataTable.getColumnType(cI), dataTable.getColumnLabel(cI));
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
        legend: {position: 'bottom'}
    };
    var lineChart = new google.visualization.LineChart(document.getElementById('lineChartDiv'));
    lineChart.draw(plotData, chartOptions);
    return false;
}

$(document).ready(function () {
    setTimeout(setAccordions, 300);
    $('#updatePlot').on('click', updatePlot);
});
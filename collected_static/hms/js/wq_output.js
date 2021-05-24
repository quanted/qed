$(document).ready(function () {

    initialize();

});

function initialize() {
    formatInputJson();
    setAccordions();
}

function formatInputJson() {
    var input = document.getElementById('inputData_P');
    input.innerHTML = syntaxHighlight(JSON.stringify(JSON.parse(input.innerHTML), undefined, 4));
}

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function setAccordions() {
    $('#collapsing-div').accordion({
        collapsible: true,
        active: 2,
        heightStyle: 'content',
    });
}

function drawChart() {
    var dataArray1 = [];
    var dataArray2 = [];
    $("#dayTable tr").each(function (idx, ele) {
        var rowData = 0;
        var hour = 0;
        var rate = 0;
        var hlife = 0;
        if (idx === 0) {
            rowData = $(ele).find('th');
            hour = rowData.eq(3).text();
            rate = rowData.eq(4).text();
            hlife = rowData.eq(5).text();
        }
        else {
            rowData = $(ele).find('td');
            hour = parseFloat(rowData.eq(3).text());
            rate = parseFloat(rowData.eq(4).text());
            hlife = parseFloat(rowData.eq(5).text());
        }
        var rowArray1 = [hour, rate];
        var rowArray2 = [hour, hlife];
        dataArray1.push(rowArray1);
        dataArray2.push(rowArray2);
    });
    var data1 = google.visualization.arrayToDataTable(dataArray1);
    var data2 = google.visualization.arrayToDataTable(dataArray2);

    var options1 = {
        // title: 'Photolysis Absorption Rate',
        // curveType: 'function',
        width: 700,
        height: 300,
        legend: 'none',
        vAxis: {title: 'Photolysis Absorption Rate', format: 'scientific', gridlines: { count: 6}},
        hAxis: {title: 'Hours', minValue: 0, maxValue: 24, gridlines: { count: 12}}
    };
    var options2 = {
        // title: 'Photolysis Half-Life',
        // curveTyle: 'function',
        width: 700,
        height: 300,
        legend: 'none',
        vAxis: {title: 'Photolysis Half-Life', format: 'scientific', gridlines: { count: 6}},
        hAxis: {title: 'Hours', minValue: 0, maxValue: 24, gridlines: { count: 12}}
    };

    var chart1 = new google.visualization.LineChart(document.getElementById('graphDiv1'));
    chart1.draw(data1, options1);
    var chart2 = new google.visualization.LineChart(document.getElementById('graphDiv2'));
    chart2.draw(data2, options2);
}


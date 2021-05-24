var baseUrl = "hms/rest/api/v3/workflow/precip_data_extraction";
var v2URL = "hms/rest/api/v3/workflow/precip_compare";

var sources = [];
var statistics = [];
var pearson_coefficients = [];
var stats = ["sum", "mean", "median", "max", "standard_deviation", "variance", "root_mean_square", "skewness", "75_percentile", "75_percentile_count",
    "95_percentile", "95_percentile_count", "99_percentile", "99_percentile_count", "zero_count"];
var mm_stats = ["sum", "mean", "median", "max", "standard_deviation", "variance", "root_mean_square", "75_percentile",
    "95_percentile", "99_percentile"];


$(function () {
    // $('#overview_block').accordion({
    //     collapsible: true,
    //     heightStyle: "content"
    // });
    // setTimeout(setOverviewTabindex, 100);

});

function setOutputUI() {
    sources = componentData.dataSource.split(", ");
    setMetadata();
    setCoefficients();
    setStatistics();
    setDataGraph2();
    var data_block_2 = document.createElement("div");
    data_block_2.id = "output_data_2";
    document.getElementById('output_data_block_table').appendChild(data_block_2);

    if (submodel === "precip_compare") {
        createCorrelationGraph();
    }
    createStatisticsTable();
    return false;
}

function getParameters() {
    var version = $('#version_select').val();
    var requestJson = {
        "dataset": "Precipitation",
        "timeLocalized": true
    };
    if (submodel === "precip_compare") {
        baseUrl = v2URL;
        requestJson["source"] = "compare";
        requestJson["dateTimeSpan"] = {
            "startDate": $("#temporal_start").val() + "-01-01",
            "endDate": $('#temporal_end').val() + "-12-31",
        };
        if ($("#source_comid").prop("checked")) {
            requestJson["geometry"] = {
                "comID": $('#location_comid').val()
            };
            requestJson["Weighted"] = $('#comid_weighted_spatial_avg').prop('checked').toString();
            requestJson["closestStation"] = $('#comid_ncdc_station').prop('checked').toString();
            if ($("#comid_ncdc_station").prop("checked")){
                requestJson["geometry"] = {
                    "StationID": $('#location_input_comid_ncdc').val()
                };
            }
        }
        else {
            requestJson["geometry"] = {
                "StationID": $('#location_ncdc').val()
            };
        }
        var resolution = $('input[name=aggregation]:checked').val();
        requestJson["temporalResolution"] = resolution;
        if (resolution === "extreme_5") {
            requestJson["ExtremeTotal"] = $('#extreme_5_total').val();
            requestJson["ExtremeDaily"] = $('#extreme_5_daily').val();
        }
        var sourceList = [];
        $('#source_list input:checked').each(function () {
            sourceList.push($(this).val());
        });
        requestJson["sourceList"] = sourceList;
    }
    else {
        requestJson["dateTimeSpan"] = {
            "startDate": $("#id_startDate").val(),
            "endDate": $('#id_endDate').val(),
        };
        requestJson["geometry"] = {
            "stationID": $("#id_stationID").val()
        };
        requestJson["source"] = "extraction";
        requestJson["sourceList"] = ["ncei","nldas", "gldas", "trmm"];
        requestJson["temporalResolution"] = $("#id_temporalresolution").val()
    }
    return requestJson;
}

// Version 2 updates
// function selectInputVersion() {
//     var selection = document.getElementById('version_select').value;
//     var v1 = document.getElementById('input_block_v1');
//     var v2 = document.getElementById('input_block_v2');
//     if (selection === '') {
//         v1.classList = 'hide';
//         v2.classList = 'hide';
//     }
//     else if (selection === 'v1') {
//         v1.classList = 'show';
//         v2.classList = 'hide';
//     }
//     else if (selection === 'v2') {
//         v1.classList = 'hide';
//         v2.classList = 'show';
//     }
//     else {
//         v1.classList = 'hide';
//         v2.classList = 'hide';
//     }
//     return false;
// }

function toggleNCEIInput() {
    var block = document.getElementById('location_input_comid_ncdc_block');
    $(block).toggle();
    if(block.style.display !== "none"){
        block.style.display = "inline-flex";
    }
}

function setCoefficients() {
    pearson_coefficients = [];
    $.map(sources, function (source1) {
        var row = [];
        $.map(sources, function (source2) {
            var key = source1 + "_" + source2 + "_pearson_coefficient";
            var coefficient = parseFloat(componentData.metadata[key]).toFixed(3);
            row.push(coefficient);
        });
        pearson_coefficients.push(row);
    });
}

function setStatistics() {
    statistics = [];
    $.map(stats, function (stat) {
        var stat_title = stat.replace(/_/g, " ");
        var units = (mm_stats.includes(stat)) ? " (mm)" : "";
        var stat_key = stat_title.charAt(0).toUpperCase() + stat_title.slice(1) + units;
        var row = [stat_key];
        $.map(sources, function (source) {
            var key = source + "_" + stat;
            var value = parseFloat(componentData.metadata[key]);
            row.push(value);
        });
        statistics.push(row);
    });
}

function createStatisticsTable() {
    var block = document.getElementById('output_data_2');
    var stats_block;
    if(document.getElementById("stats_block")){
        stats_block = document.getElementById("stats_block");
        while(stats_block.lastChild){
            stats_block.removeChild(stats_block.lastChild);
        }
    }
    else {
        stats_block = document.createElement("div");
    }
    stats_block.id = "stats_block";
    block.appendChild(stats_block);

    var stats_title = document.createElement("h3");
    stats_title.id = "stats_title";
    stats_title.innerHTML = "Statistic For Data Sources";
    stats_block.appendChild(stats_title);

    var stats_container = document.createElement("div");
    stats_container.id = "stats_container";
    stats_block.appendChild(stats_container);

    var statsDataTable = new google.visualization.DataTable();
    statsDataTable.addColumn('string', 'Statistic');
    $.map(sources, function (source) {
        statsDataTable.addColumn('number', source.toUpperCase());
    });
    statsDataTable.addRows(statistics);
    var tableOptions = {
        title: "Statistics For Data Sources",
        // pageSize: 10,
        width: '100%'
    };
    var statsTable = new google.visualization.Table(stats_container);
    statsTable.draw(statsDataTable, tableOptions);
    return false;

}

function createCorrelationGraph() {
    var labels = sources;
    var data = pearson_coefficients;

    var matrix_block;
    if (document.getElementById("matrix_block")){
        matrix_block = document.getElementById("matrix_block");
        while(matrix_block.lastChild){
            matrix_block.removeChild(matrix_block.lastChild);
        }
    }
    else {
        matrix_block = document.createElement("div");
    }
    matrix_block.id = "matrix_block";
    document.getElementById('output_data_2').appendChild(matrix_block);

    var matrix_title = document.createElement("h3");
    matrix_title.id = "matrix_title";
    matrix_title.innerHTML = "Pearson's Correlation Coefficients";
    matrix_block.appendChild(matrix_title);

    var matrix_container = document.createElement("div");
    matrix_container.id = "matrix_container";
    matrix_block.appendChild(matrix_container);

    var matrix_legend = document.createElement("div");
    matrix_legend.id = "matrix_legend";
    matrix_block.appendChild(matrix_legend);

    createMatrix({
        container: '#matrix_container',
        data: data,
        labels: labels,
        start_color: '#369FE5',
        end_color: '#194969'
    });

}

//TESTING
function getTestData() {
    componentData = test_data;
    console.log("Task successfully completed and data was retrieved.");
    setOutputUI();
    $('#component_tabs').tabs("enable", 2);
    $('#component_tabs').tabs("option", "active", 2);
    dyGraph.resize();
    // counter = 25;
}

// Copied from https://bl.ocks.org/arpitnarechania/caeba2e6579900ea12cb2a4eb157ce74, open source d3 examples
function createMatrix(options) {
    var margin = {top: 50, right: 50, bottom: 100, left: 100},
        width = 350,
        height = 350,
        data = options.data,
        container = options.container,
        labelsData = options.labels,
        startColor = options.start_color,
        endColor = options.end_color;

    var widthLegend = 100;

    if (!data) {
        throw new Error('Please pass data');
    }

    if (!Array.isArray(data) || !data.length || !Array.isArray(data[0])) {
        throw new Error('It should be a 2-D array');
    }

    var maxValue = d3.max(data, function (layer) {
        return d3.max(layer, function (d) {
            return d;
        });
    });
    var minValue = d3.min(data, function (layer) {
        return d3.min(layer, function (d) {
            return d;
        });
    });

    var numrows = data.length;
    var numcols = data[0].length;

    var svg = d3.select(container).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var background = svg.append("rect")
        .style("stroke", "black")
        .style("stroke-width", "2px")
        .attr("width", width)
        .attr("height", height);

    var x = d3.scaleBand()
        .domain(d3.range(numcols))
        .range([0, width]);

    var y = d3.scaleBand()
        .domain(d3.range(numrows))
        .range([0, height]);

    var colorMap = d3.scaleLinear()
        .domain([minValue, maxValue])
        .range([startColor, endColor]);

    var row = svg.selectAll(".row")
        .data(data)
        .enter().append("g")
        .attr("class", "row")
        .attr("transform", function (d, i) {
            return "translate(0," + y(i) + ")";
        });

    var cell = row.selectAll(".cell")
        .data(function (d) {
            return d;
        })
        .enter().append("g")
        .attr("class", "cell")
        .attr("transform", function (d, i) {
            return "translate(" + x(i) + ", 0)";
        });

    cell.append('rect')
        .attr("width", x.bandwidth())
        .attr("height", y.bandwidth())
        .style("stroke-width", 0);

    cell.append("text")
        .attr("dy", ".32em")
        .attr("x", x.bandwidth() / 2)
        .attr("y", y.bandwidth() / 2)
        .attr("text-anchor", "middle")
        .style("fill", function (d, i) {
            return d >= maxValue / 2 ? 'white' : 'black';
        })
        .text(function (d, i) {
            return d;
        });

    row.selectAll(".cell")
        .data(function (d, i) {
            return data[i];
        })
        .style("fill", colorMap);

    var labels = svg.append('g')
        .attr('class', "labels");

    var columnLabels = labels.selectAll(".column-label")
        .data(labelsData)
        .enter().append("g")
        .attr("class", "column-label")
        .attr("transform", function (d, i) {
            return "translate(" + x(i) + "," + height + ")";
        });

    columnLabels.append("line")
        .style("stroke", "black")
        .style("stroke-width", "1px")
        .attr("x1", x.bandwidth() / 2)
        .attr("x2", x.bandwidth() / 2)
        .attr("y1", 0)
        .attr("y2", 5);

    columnLabels.append("text")
        .attr("x", 0)
        .attr("y", y.bandwidth() / 2)
        .attr("dy", ".82em")
        .attr("text-anchor", "end")
        .attr("transform", "rotate(-60)")
        .text(function (d, i) {
            return d;
        });

    var rowLabels = labels.selectAll(".row-label")
        .data(labelsData)
        .enter().append("g")
        .attr("class", "row-label")
        .attr("transform", function (d, i) {
            return "translate(" + 0 + "," + y(i) + ")";
        });

    rowLabels.append("line")
        .style("stroke", "black")
        .style("stroke-width", "1px")
        .attr("x1", 0)
        .attr("x2", -5)
        .attr("y1", y.bandwidth() / 2)
        .attr("y2", y.bandwidth() / 2);

    rowLabels.append("text")
        .attr("x", -8)
        .attr("y", y.bandwidth() / 2)
        .attr("dy", ".32em")
        .attr("text-anchor", "end")
        .text(function (d, i) {
            return d;
        });

    var key = d3.select("#matrix_legend")
        .append("svg")
        .attr("width", widthLegend)
        .attr("height", height + margin.top + margin.bottom);

    var legend = key
        .append("defs")
        .append("svg:linearGradient")
        .attr("id", "gradient")
        .attr("x1", "100%")
        .attr("y1", "0%")
        .attr("x2", "100%")
        .attr("y2", "100%")
        .attr("spreadMethod", "pad");

    legend
        .append("stop")
        .attr("offset", "0%")
        .attr("stop-color", endColor)
        .attr("stop-opacity", 1);

    legend
        .append("stop")
        .attr("offset", "100%")
        .attr("stop-color", startColor)
        .attr("stop-opacity", 1);

    key.append("rect")
        .attr("width", widthLegend / 2 - 10)
        .attr("height", height)
        .style("fill", "url(#gradient)")
        .attr("transform", "translate(0," + margin.top + ")");

    var y = d3.scaleLinear()
        .range([height, 0])
        .domain([minValue, maxValue]);

    var yAxis = d3.axisRight().scale(y);

    key.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(41," + margin.top + ")")
        .call(yAxis);
}

function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}
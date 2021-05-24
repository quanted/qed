// -------------- MAP code -------------- //
// initialize the map
var map = L.map('map', {renderer: L.svg({padding: 100})}).setView([33.926250, -83.356552], 5);

// load basemap
var layer = null;
setBasemap('Imagery');
addStreams();
// var layer = L.esri.basemapLayer('Imagery').addTo(map);
var layerLabels;

function setOutputUI(){
    //setOutputPage();
    setMetadata();
    setDataGraph2();
    return false;
}

function setBasemap(basemap) {
    if (layer) {
        map.removeLayer(layer);
    }
    layer = L.esri.basemapLayer(basemap);

    map.addLayer(layer);

    if (layerLabels) {
        map.removeLayer(layerLabels);
    }

    if (basemap === 'ShadedRelief' || basemap === 'Imagery' || basemap === 'Terrain'
    ) {
        layerLabels = L.esri.basemapLayer(basemap + 'Labels');
        map.addLayer(layerLabels);
    }
}

function changeBasemap(basemaps) {
    var basemap = basemaps.value;
    setBasemap(basemap);
    addStreams();
}

// ------------ STREAM NETWORK code ------------- //

function addStreams() {
    L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
        layers: 4,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }).addTo(map);
}

// ------------ STREAM NETWORK INFO code ------------- //

var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'stream_info');
    this.update();
    return this._div;
};
info.update = function (props) {
    this._div.innerHTML = '<h5>Stream Network Details</h5>' +
        '<table id="stream_info_table" style="margin-bottom: 0px !important; background: none !important;"> ' +
        '<tr><td class="startCOMID_color">Start COMID:</td> <td id="startCOMIDVal"></td></tr>' +
        '<tr><td class="endCOMID_color">End COMID:</td><td id="endCOMIDVal"></td></tr>' +
        '<tr><td>Network Length:</td><td id="lengthVal"></td></tr>' +
        '<tr><td>Network Flowtime:</td><td id="flowtimeVal"></td></tr>' +
        '<tr><td>Total Stream Segments:</td><td id="segmentCount"></td></tr></table>';
};
info.addTo(map);

// ------------ Main JS ------------- //
var baseUrl = 'hms/rest/api/v3/workflow/timeoftravel/';
var counter = 100;
var jobID = null;

var startCOMID = null;
var endCOMID = null;
var startLayer = null;
var endLayer = null;
var networkLayer = null;

var lat = null;
var lng = null;

var table = null;
var data = null;
var tableData = null;

var selectedRow = null;
var selectedCol = null;

initializeForms();
createInputTable();
setTableData(true);

$(function () {
    $('#overview_block').accordion({
        collapsible: true,
        heightStyle: "content"
    });
    $("#component_tabs").on("tabsactivate", function(event, ui){
        map.invalidateSize(true);
    });
    map.on("click", function (e){
        onStreamMapClick(e);
    });

    $('#id_startCOMID').on("blur", function(event, ui){
        getStreamNetworkByCOMID($('#id_startCOMID').val());
    });
    $('#id_endCOMID').on("blur", function(event, ui){
        getStreamNetworkByCOMID($('#id_endCOMID').val());
    });

    $('#start_del').on("click", function(event, ui){
       deleteCOMID(true);
    });
    $('#end_del').on("click", function(event, ui){
       deleteCOMID(false);
    });
    $('#open_table_button').on("click", function(event, ui){
       $('#backdrop').show();
    });
    $('#backdrop_exit').on("click", function(event, ui){
        $('#backdrop').hide();
    });
    $('#id_startDate').on("change", function(event, ui){
        setTableData(false);
    });
    $('#id_endDate').on("change", function(event, ui){
        setTableData(false);
    });
    $('#id_startHour').on("change", function(event, ui){
        setTableData(false);
    });
    $('#id_endHour').on("change", function(event, ui){
        setTableData(false);
    });

    $('#backdrop_table_div').on('click', 'td', function (e) {
        var selection = table.getSelection();
        if(selection.length === 0){
            return;
        }
        var cell = e.target;
        selectedRow = selection[0].row;
        selectedCol = cell.cellIndex;
        var v = this.innerHTML;
        if (!v.includes('<input') && $(this).index() === 2) {
            this.innerHTML = "<input id='tblCell' class='tblCellEdit' onfocus='this.value = this.value;' type='text' value='" + v + "'/>";
            document.getElementById('tblCell').focus();
        }
    });
    //
    $('#backdrop_table_div').on('blur', 'td', function (e) {
        var v = Number(this.childNodes[0].value);
        this.innerHTML = v;
        tableData[selectedRow][selectedCol] = v;
        drawTable();
        selectedRow = null;
        selectedCol = null;
    });
    $('.ui-tabs-tab').on("click", function(e){
        $('#backdrop').hide();
    });

});

function initializeForms(){
    var start = $('#id_startCOMID').parent();
    var end = $('#id_endCOMID').parent();
    var startDel = document.createElement("div");
    startDel.id = "start_del";
    startDel.innerHTML = "x";
    startDel.className = "deleteCOMID";
    var endDel = document.createElement("div");
    endDel.id = "end_del";
    endDel.innerHTML = "x";
    endDel.className = "deleteCOMID";

    $(start).append(startDel);
    $(end).append(endDel);

    var startDate = new Date();
    var endDate = new Date();
    startDate.setHours(startDate.getHours() + 1);
    endDate.setHours(endDate.getHours() + 19);
    var startString = startDate.getFullYear() + "-" + (((startDate.getMonth() + 1) < 10 ? '0' : '') + (startDate.getMonth() + 1)) + "-" + (((startDate.getDate() + 1) < 10 ? '0' : '') + (startDate.getDate() + 1));
    $("#id_startDate").val(startString);
    var endString = endDate.getFullYear() + "-" + (((endDate.getMonth() + 1) < 10 ? '0' : '') + (endDate.getMonth() + 1)) + "-" + (((endDate.getDate() + 1) < 10 ? '0' : '') + (endDate.getDate() + 1));
    $("#id_endDate").val(endString);
    $("#id_startHour").val((startDate.getHours() < 10 ? '0' : '') + startDate.getHours());
    $("#id_endHour").val((endDate.getHours() < 10 ? '0' : '') + endDate.getHours());
}

function addZero(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

function setTableData(initial){
    var startDate = new Date($('#id_startDate').val());
    startDate.setHours(Number($('#id_startHour').val()));

    var endDate = new Date($('#id_endDate').val());
    endDate.setHours(Number($('#id_endHour').val()));

    var timesteps = [];
    var currentDate = startDate;
    while (currentDate.getTime() < endDate.getTime()){
        var date = currentDate.getFullYear() + "-" + (currentDate.getMonth()+1) + "-" + currentDate.getDate();
        var hour = currentDate.getHours();
        var timestep = [date, hour, 0];
        timesteps.push(timestep);
        currentDate.setHours(currentDate.getHours() + 1);
    }
    tableData = timesteps;
    if(!initial){
        drawTable();
    }
}

function deleteCOMID(start){
    if(start){
        startCOMID = null;
        endCOMID = null;
        $('#startCOMIDVal').html("");
        $('#endCOMIDVal').html("");
        $('#lengthVal').html("");
        $('#flowtimeVal').html("");
        $('#segmentCount').html("");

        $('#id_startCOMID').val("");
        $('#id_endCOMID').val("");
        if (map.hasLayer(startLayer)) {
            map.removeLayer(startLayer);
            startLayer = null;
        }
        if(map.hasLayer(networkLayer)){
            map.removeLayer(networkLayer);
            networkLayer = null;
        }
        if (map.hasLayer(endLayer)) {
            map.removeLayer(endLayer);
            endLayer = null;
        }
    }
    else{
        endCOMID = null;
        $('#endCOMIDVal').html("");
        $('#lengthVal').html("");
        $('#flowtimeVal').html("");
        $('#segmentCount').html("");

        $('#id_endCOMID').val("");
        if(map.hasLayer(networkLayer)){
            map.removeLayer(networkLayer);
            networkLayer = null;
        }
        if (map.hasLayer(endLayer)) {
            map.removeLayer(endLayer);
            endLayer = null;
        }
    }
}

function getParameters(){
    var timeseries = dataToCSV();
    var requestJson = {
        "csrfmiddlewaretoken": getCookie("csrftoken"),
        "source": "NWM",
        "dateTimeSpan": {
            "startDate": $("#id_startDate").val() + " " + $('#id_startHour').val(),
            "endDate": $('#id_endDate').val() + " " + $('#id_endHour').val()
        },
        "geometry": {
            "geometryMetadata": {
                "startCOMID": $("#id_startCOMID").val(),
                "endCOMID": $('#id_endCOMID').val()
            }
        },
        "contaminantInflow": tableData,
        "inflowSource": $("#id_inflowSource").val(),
        "units": "default",
        "outputFormat": "json"
    };
    return requestJson;
}

function getData() {
    var params = getParameters();
    var jsonParams = JSON.stringify(params);
    $.ajax({
        type: "POST",
        url: baseUrl,
        accepts: "application/json",
        data: jsonParams,
        processData: false,
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            jobID = taskID;//data.job_id;
            console.log("Data request success. Task ID: " + jobID);
            toggleLoader(false, "Processing data request. Task ID: " + jobID);
            setTimeout(getDataPolling, 30000);
            $('#workflow_tabs').tabs("enable", 2);
            $('#workflow_tabs').tabs("option", "active", 2);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Data request error...");
            console.log(errorThrown);
        },
        complete: function (jqXHR, textStatus) {
            console.log("Data request complete");
        }
    });
    return false;
}

function getDataPolling() {
    //counter = counter - 1;
    var requestUrl = "hms/rest/api/v2/hms/data";
    jobID = taskID;
    if (counter > 0) {
        $.ajax({
            type: "GET",
            url: requestUrl + "?job_id=" + jobID,
            accepts: "application/json",
            timeout: 0,
            contentType: "application/json",
            success: function (data, textStatus, jqXHR) {
                if (data.status === "SUCCESS") {
                    if (typeof data.data === "string") {
                        jobData = JSON.parse(data.data);
                    }else{
                        jobData = data.data;
                    }
                    setOutputPage();
                    console.log("Task successfully completed and data was retrieved.");
                    // dyGraph.resize();
                    // counter = 25;
                }
                else if (data.status === "FAILURE") {
                    toggleLoader(false, "Task " + jobID + " encountered an error.");
                    console.log("Task failed to complete.");
                }
                else {
                    setTimeout(getDataPolling, 10000);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Data request error...");
                console.log(errorThrown);
                toggleLoader(false, "Error retrieving data for task ID: " + jobID);
            },
            complete: function (jqXHR, textStatus) {
                console.log("Data request complete");
            }
        });
    }
    else {
        console.log("Failed to get data, reached polling cap.")
    }
    return false;
}

function onStreamMapClick(e) {
    lat = Number(e.latlng.lat).toFixed(6);
    lng = Number(e.latlng.lng).toFixed(6);
    setTimeout(onLoader, 10);
    setTimeout(getStreamSegment, 20);
}

function getStreamSegment() {
    var url = 'https://ofmpub.epa.gov/waters10/PointIndexing.Service';
    var latitude = lat.toString();
    var longitude = lng.toString();
    var ptIndexParams = {
        'pGeometry': 'POINT(' + longitude + ' ' + latitude + ')',
        'pGeometryMod': 'WKT,SRSNAME=urn:ogc:def:crs:OGC::CRS84',
        'pPointIndexingMethod': 'DISTANCE',
        'pPointIndexingMaxDist': 25,
        'pOutputPathFlag': 'TRUE',
        'pReturnFlowlineGeomFlag': 'TRUE',
        'optOutCS': 'SRSNAME=urn:ogc:def:crs:OGC::CRS84',
        'optOutPrettyPrint': 0
    };
    $.ajax({
        type: 'GET',
        url: url,
        jsonp: true,
        data: ptIndexParams,
        async: false,
        success: function (data, status, jqXHR) {
            $('#error_block').html("");
            var streamData = data;
            if(!typeof(data) === "object") {
                streamData = JSON.parse(data);
            }
            createStreamSeg(streamData, false);

            return data;
        },
        error: function (jqXHR, status) {
            $('#error_block').html('Unable to get the stream segment closest to point: ' + latitude + ', ' + longitude);
            setTimeout(offLoader, 10);
            return null;
        }
    });
}

function getStreamNetwork(){
    var rest_url = 'https://ofmpub.epa.gov/waters10/Navigation.Service';
    var data = {
        pNavigationType: "PP",
        pStartComID: startCOMID,
        pStopComid: endCOMID,
        pReturnFlowlineAttr: "TRUE"
    };
    $.ajax({
        type: 'GET',
        url: rest_url,
        jsonp: true,
        data: data,
        async: false,
        success: function (data, status, jqXHR) {
            $('#error_block').html("");
            var streamData = data;
            if(!typeof(data) === "object") {
                streamData = JSON.parse(data);
            }
            if(streamData.output.ntNavResultsStandard.length <=1){
                $('#error_block').html('Start and end COMIDs are not valid for connected stream network');
                setTimeout(offLoader, 10);
                endCOMID = null;
                return null;
            }
            addStreamNetwork(streamData);
            return data;
        },
        error: function (jqXHR, status) {
            $('#error_block').html('Start and end COMIDs are not valid for connected stream network');
            setTimeout(offLoader, 10);
            endCOMID = null;
            return null;
        }
    });
}

function getStreamNetworkByCOMID(comid){
    var rest_url = 'https://ofmpub.epa.gov/waters10/Navigation.Service';
    var data = {
        pNavigationType: "PP",
        pStartComID: comid,
        pStopComid: comid,
        pReturnFlowlineAttr: "TRUE"
    };
    $.ajax({
        type: 'GET',
        url: rest_url,
        jsonp: true,
        data: data,
        async: false,
        success: function (data, status, jqXHR) {
            $('#error_block').html("");
            var streamData = data;
            if(!typeof(data) === "object") {
                streamData = JSON.parse(data);
            }
            createStreamSeg(streamData, true);

            return data;
        },
        error: function (jqXHR, status) {
            $('#error_block').html('Start and end COMIDs are not valid for connected stream network');
            setTimeout(offLoader, 10);
            endCOMID = null;
            return null;
        }
    });
}

function createStreamSeg(streamData, fromCOMID){
    if (startCOMID === null || endCOMID !== null){
        startCOMID = streamData.output.ary_flowlines[0].comid;
        $('#startCOMIDVal').html(startCOMID);
        $('#endCOMIDVal').html("");
        $('#lengthVal').html("");
        $('#flowtimeVal').html("");
        $('#segmentCount').html("");

        endCOMID = null;
        $('#id_endCOMID').val("");
        $('#id_startCOMID').val(startCOMID);
        addStreamSeg(streamData, true, fromCOMID);
    }
    else{
        endCOMID = streamData.output.ary_flowlines[0].comid;
        $('#endCOMIDVal').html(endCOMID);
        getStreamNetwork();
        if(endCOMID !== null) {
            $('#id_endCOMID').val(endCOMID);
            addStreamSeg(streamData, false, fromCOMID);
        }
    }
}

function addStreamSeg(streamData, start, fromCOMID) {
    if(fromCOMID){
        var latlon = streamData.output.ntNavResultsStandard[0].shape.coordinates.map(function (c) {
            return c.reverse();
        });
    }
    else {
        var latlon = streamData.output.ary_flowlines[0].shape.coordinates.map(function (c) {
            return c.reverse();
        });
    }
    if (map.hasLayer(startLayer) && start === true) {
        map.removeLayer(startLayer);
        if(map.hasLayer(networkLayer)){
            map.removeLayer(networkLayer);
        }
    }
    if (map.hasLayer(endLayer)) {
        map.removeLayer(endLayer);
    }

    if(start === true){
        startLayer = L.polyline(latlon, {
            color: '#00D827',
            weight: 7,
            opacity: 0.9,
            lineJoin: 'round'
        }).addTo(map);
    }
    else {
        endLayer = L.polyline(latlon, {
            color: '#D80000',
            weight: 7,
            opacity: 0.9,
            lineJoin: 'round'
        }).addTo(map);
        map.fitBounds(networkLayer.getBounds());
    }
    setTimeout(offLoader, 10);
}

function addStreamNetwork(streamData) {
    var streamLayers = [];
    streamData.output.ntNavResultsStandard.map(function(c){
       var rpoints = c.shape.coordinates.map(function(p){
           return p.reverse();
       });
       var path = L.polyline(rpoints, {
            color: '#0048D8',
            weight: 4,
            opacity: 0.9,
            lineJoin: 'round'
        });
        streamLayers.push(path);
    });

    $('#lengthVal').html(streamData.output.total_distance_km + " (km)");
    $('#flowtimeVal').html(streamData.output.total_flowtime_day + " (days)");
    $('#segmentCount').html(parseInt(streamLayers.length));

    if (map.hasLayer(networkLayer)) {
        map.removeLayer(networkLayer);
        networkLayer = null;
    }
    networkLayer = L.featureGroup(streamLayers);
    networkLayer.addTo(map);
    startLayer.bringToFront();
    map.fitBounds(networkLayer.getBounds());
    setTimeout(offLoader, 10);

}

function onLoader(){
    $('#map_loader').show();
    setTimeout(offLoader, 3000);
}

function offLoader(){
    $('#map_loader').hide();
}

function createInputTable(){
    var input_table = $('.input_table');
    var timeSeriesTableRow = document.createElement('dev');
    timeSeriesTableRow.classList.add('input_table_row');
    var openTableButton = document.createElement('input');
    openTableButton.classList.add("open_table");
    openTableButton.id = 'open_table_button';
    openTableButton.value = 'Open Input Table';
    $(timeSeriesTableRow).append(openTableButton);
    $(input_table).append(timeSeriesTableRow);

    var backdrop = document.createElement('div');
    backdrop.id = "backdrop";
    var backdropExit = document.createElement('div');
    backdropExit.id = "backdrop_exit";
    backdropExit.innerHTML = "x";
    var backdropTableDiv = document.createElement('div');
    backdropTableDiv.id = "backdrop_table_div";
    $(backdrop).append(backdropExit);
    $(backdrop).append(backdropTableDiv);
    $('#main-column').append(backdrop);
}

// Load the Visualization API and the piechart package.
google.charts.load('current', {'packages':['table']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawTable);

function drawTable(){
    data = new google.visualization.DataTable();
    data.addColumn('string', 'Date');
    data.addColumn('number', 'Hour');
    data.addColumn('number', 'Contaminant Inflow');
    data.addRows(tableData);

    table = new google.visualization.Table(document.getElementById('backdrop_table_div'));
    table.draw(data, {showRowNumber: false, width: '100%', height: '100%', sort: 'disable', page: 'enable', pageSize: 18});
}

function dataToCSV(){
    return google.visualization.dataTableToCsv(data);
}

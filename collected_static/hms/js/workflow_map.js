// --- Page Variables --- //
// initialize the map
var map = L.map('map', {renderer: L.svg({padding: 100})}).setView([40.265306, -98.623725], 5);

// load basemap
L.esri.basemapLayer('Topographic').addTo(map);

// load huc watershed boundaries

var currentInputLayer;
var secondaryInputLayer = "";

var layerESRI = L.esri.basemapLayer('Imagery');
var layerLabels;

var huc8;
var comid;
var streamData;
var workflowData;

var selectedStream;

var datatableData;
var dataTableMetadata;

google.charts.load('current', {'packages': ['table']});

// -- Map functions -- //
function onEachFeatureClick(feature, layer) {
    layer.on('click', function (e) {
        if ((this.currentHUC !== feature.properties.HUC_8 || this.currentHUC === null) || secondaryInputLayer !== "") {
            this.currentHUC = feature.properties.HUC_8;
            var hucs = [];
            hucs.push(feature.properties.HUC_8);
            var latitude = Number(e.latlng.lat).toFixed(6);
            var longitude = Number(e.latlng.lng).toFixed(6);
            selectHUCs(hucs, latitude, longitude);
            huc8 = feature.properties.HUC_8;
            $('#hucID').html("Huc 8 ID: <a href='https://cfpub.epa.gov/surf/huc.cfm?huc_code=" + feature.properties.HUC_8 + "' target='_blank'>" +
                feature.properties.HUC_8 + "</a>");
        }
        else {
            if (secondaryInputLayer !== "") {
                map.removeLayer(secondaryInputLayer);
            }
            secondaryInputLayer = "";
            resetHUCLayer();
            this.currentHUC = null;
        }
    });
}

function setBasemap(basemap) {
    if (layerESRI) {
        map.removeLayer(layerESRI);
    }
    layerESRI = L.esri.basemapLayer(basemap);
    map.addLayer(layerESRI);
    if (layerLabels) {
        map.removeLayer(layerLabels);
    }
    if (basemap === 'ShadedRelief' || basemap === 'Imagery' || basemap === 'Terrain') {
        layerLabels = L.esri.basemapLayer(basemap + 'Labels');
        map.addLayer(layerLabels);
    }
}

function changeBasemap(basemaps) {
    var basemap = basemaps.value;
    setBasemap(basemap);
    updateInputLayer();
}

//style HUC 8 polygon
function getColor(d) {
    return '#93D4BC'
}

//style HUC 8 polygon cont.
function hucStyle(feature) {
    return {
        fillColor: getColor(feature.properties.NumbSpc),
        weight: .3,
        opacity: 0.9,
        color: 'black',
        fillOpacity: 0.3
    };
}

function resetHUCLayer() {
    currentInputLayer.eachLayer(function (layer) {
        currentInputLayer.resetStyle(layer);
    });
}

//style selected HUC 8 polygon
function selectHUCs(hucs, lat, lng) {
    resetHUCLayer();
    var layerGroup = [];
    var hucObject = currentInputLayer.getLayers();
    var l = 46; // layers start at layerID = 46
    var r = hucObject.length + l;
    $.each(hucs, function (index, value) {
        var resultIdx = binarySearch(l, r, value);
        if (resultIdx !== -1) {
            currentInputLayer.getLayer(resultIdx).setStyle({
                color: 'black',
                weight: 0.7,
                fillColor: '#0979D9',
                fillOpacity: 0.4
            });
            layerGroup.push(currentInputLayer.getLayer(resultIdx));
        }
    });
    var selection = document.getElementById("inputLayer");
    var layerSelected = selection.options[selection.selectedIndex].value;
    if (layerSelected.localeCompare("catchment") === 0 && secondaryInputLayer === "") {
        secondaryInputLayer = L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
            layers: 4,
            format: 'image/png',
            minZoom: 0,
            maxZoom: 18,
            transparent: true
        }).addTo(map);
        map.fitBounds(L.featureGroup(layerGroup).getBounds());

    }
    else if (layerSelected.localeCompare("catchment") === 0) {
        var url = "https://ofmpub.epa.gov/waters10/PointIndexing.Service";
        var ptIndexParams = {
            'pGeometry': 'POINT(' + lng + ' ' + lat + ')'
            , 'pGeometryMod': 'WKT,SRSNAME=urn:ogc:def:crs:OGC::CRS84'
            , 'pPointIndexingMethod': 'DISTANCE'
            , 'pPointIndexingMaxDist': 25
            , 'pOutputPathFlag': 'TRUE'
            , 'pReturnFlowlineGeomFlag': 'TRUE'
            , 'optOutCS': 'SRSNAME=urn:ogc:def:crs:OGC::CRS84'
            , 'optOutPrettyPrint': 0
        };
        $.ajax({
            type: "GET",
            url: url,
            jsonp: true,
            data: ptIndexParams,
            async: false,
            success: function (data, status, jqXHR) {
                streamData = JSON.parse(data);
                comid = streamData.output.ary_flowlines[0].comid;
                $('#comid').html("Steam segment comid: " + comid);
                addStreamSeg(streamData);
                enableTab($('#date-title'));
            },
            error: function (jqXHR, status) {
                console.log("Error retrieving stream segment data.");
            }
        });
    }
    else {
        map.fitBounds(L.featureGroup(layerGroup).getBounds());
        enableTab($('#date-title'));
    }
}

function addStreamSeg(streamData) {
    var latlon = streamData.output.ary_flowlines[0].shape.coordinates.map(function (c) {
        return c.reverse();
    });
    var huc8geom;
    if (huc8[0][0] < 0) {
        huc8geom = huc8.map(function (c) {
            return c.reverse();
        });
    }
    if (map.hasLayer(selectedStream)) {
        map.removeLayer(selectedStream);
    }

    selectedStream = L.polyline(latlon, {
        color: '#02bfe7',
        weight: 5,
        opacity: 0.9,
        lineJoin: 'round'
    }).addTo(map);
    // streamHuc = L.polygon(huc8geom, {
    //     color: 'white',
    //     weight: 2,
    //     opacity: 0.9,
    //     fillColor: '#9ecae1',
    //     fillOpacity: 0.3
    // }).addTo(map);
    map.fitBounds(selectedStream.getBounds());
}

function binarySearch(left, right, value) {
    while (left <= right) {
        var mid = Math.floor((left + right) / 2);
        if (currentInputLayer.hasLayer(mid)) {
            var midValue = Number(currentInputLayer.getLayer(mid).feature.properties.HUC_8);
            if (Number(midValue) === Number(value)) {
                return mid;
            }
            else if (Number(midValue) > Number(value)) {
                right = mid - 1;
            }
            else {
                left = mid + 1;
            }
        }
        else {
            return -1;
        }
    }
    return -1;
}

function updateInputLayer() {
    // startLoader();
    $("#inputSearchBlock").hide();
    $('#data-display-button-div').hide();
    $('#input-description').html("");
    setAccordion();
    if (currentInputLayer == null) {
    }
    else {
        map.removeLayer(currentInputLayer);
    }
    if (secondaryInputLayer === "") {
    }
    else {
        map.removeLayer(secondaryInputLayer);
    }
    var selection = document.getElementById("inputLayer");
    var layerSelected = selection.options[selection.selectedIndex].value;
    if (layerSelected.localeCompare("none") === 0) {
        $('#hucID').html("");
        $('#comid').html("");
        if (selectedStream !== "") {
            map.removeLayer(selectedStream);
        }
        selectedStream = null;
    }
    else if (layerSelected.localeCompare("huc8") === 0) {
        $("#inputSearchType").html("HUC 8 ID");
        $('#geometry-title').removeClass("ui-state-disabled");
        currentInputLayer = L.geoJson(huc8s, {
            style: hucStyle,
            onEachFeature: onEachFeatureClick
        }).addTo(map);
        $('#input-description').html("Select a huc 8 by clicking on the map or entering a huc 8 ID in the search box.");
        $("#inputSearchBlock").show();
        $('#geometry-title').trigger("click");
    }
    else if (layerSelected.localeCompare("catchment") === 0) {
        $("#inputSearchType").html("HUC 8 ID");
        $('#geometry-title').removeClass("ui-state-disabled");
        currentInputLayer = L.geoJson(huc8s, {
            style: hucStyle,
            onEachFeature: onEachFeatureClick
        }).addTo(map);
        $("#input-description").html("Select a huc 8 by clicking on the map or entering a huc 8 ID in the search box. Once a huc has been selected zoom into your area of interest and select the stream segment for your catchment.");
        $("#inputSearchBlock").show();
        $('#geometry-title').trigger("click");
    }
    else if (layerSelected.localeCompare("streamNetwork") === 0) {
        $("#inputSearchType").html("Stream segment ID");
        $('#geometry-title').removeClass("ui-state-disabled");
        currentInputLayer = L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
            layers: 4,
            format: 'image/png',
            minZoom: 0,
            maxZoom: 18,
            transparent: true
        }).addTo(map);
        $("#inputSearchBlock").show();
        $('#geometry-title').trigger("click");
    }
    else {
        // do something else
    }
    // stopLoader();
    return false;
}

function setAccordion() {
    // Also functions as disableTab
    $('#workflow-inputs').accordion(
        {
            header: "h3",
            collapsible: true,
            active: false,
            animate: 300
        });
    $('#geometry-title').addClass("ui-state-disabled");
    $('#date-title').addClass("ui-state-disabled");
    $('#dataset-title').addClass("ui-state-disabled");
    $('#source-title').addClass("ui-state-disabled");
    $('#options-title').addClass("ui-state-disabled");
    $('#data-request').hide();
    $('#inputSearch').val("");
    $('#workflow-inputs').show();
}

function enableTab(tab) {
    $(tab).removeClass("ui-state-disabled");
    $(tab).trigger('click');
}

function startLoader() {
    $('#loading-div').show();
    // setTimeout(600, stopLoader);
}

function stopLoader() {
    $('#loading-div').hide();
}

function setDatePickers() {
    var options = {autoSize: true};
    $('#startDate').datepicker(options);
    $('#endDate').datepicker(options);
}

function validateDates() {
    $('#date-input-error').html("");
    var startDate = new Date($('#startDate').val());
    var endDate = new Date($('#endDate').val());
    if (!isNaN(startDate.getDate()) && !isNaN(endDate.getDate())) {
        if ((endDate > startDate)) {
            enableTab($('#dataset-title'));
        }
        else {
            $('#date-input-error').html("Invalid date range, start date must be before end date.");
        }
    }
}

function validateDataset() {
    var dataset = $('#dataset-input').val();
    if (dataset !== "") {
        enableTab($("#source-title"));
    }
}

function validateSource() {
    var source = $('#source-input').val();
    if (source !== "") {
        enableTab($("#options-title"));
        enableSubmission();
    }
}

function enableSubmission() {
    $('#data-request').show();
}

function getData() {
    $('#data-request-error').html("");
    $('#data-request-success').html("");
    startLoader();
    var dataset = $('#dataset-input').val();
    // var baseUrl = "http://127.0.0.1:8000/hms/rest/api/hydrology/" + dataset;
    var baseUrl = "https://qedinternal.epa.gov/hms/rest/api/hydrology/" + dataset;
    var startDate = $('#startDate').val();
    var endDate = $('#endDate').val();
    var source = $('#source-input').val();
    var temporalResolution = document.getElementById("temporal-resolution").options[document.getElementById("temporal-resolution").selectedIndex].value;
    var timeLocalized = document.getElementById("time-localized").options[document.getElementById("time-localized").selectedIndex].value;
    var requestData;
    var selection = document.getElementById("inputLayer");
    var layerSelected = selection.options[selection.selectedIndex].value;
    // requestData = {
    //     "geometryType": "test",
    //     "geometryInput": huc8,
    //     "source": source,
    //     "dateTimeSpan": {
    //         "startDate": startDate,
    //         "endDate": endDate
    //     },
    //     "timeLocalized": timeLocalized,
    //     "temporalResolution": temporalResolution
    // };
    if (layerSelected == "catchment") {
        requestData = {
            "geometryInputs": {
                "huc8": huc8,
                "commid": comid
            },
            "source": source,
            "dateTimeSpan": {
                "startDate": startDate,
                "endDate": endDate
            },
            "timeLocalized": timeLocalized,
            "temporalResolution": temporalResolution
        };
    }
    else {
        requestData = {
            "geometryType": "test",
            "geometryInput": huc8,
            "source": source,
            "dateTimeSpan": {
                "startDate": startDate,
                "endDate": endDate
            },
            "timeLocalized": timeLocalized,
            "temporalResolution": temporalResolution
        };
    }
    requestData = JSON.stringify(requestData);
    $.ajax({
        url: baseUrl,
        data: requestData,
        dataType: 'json',
        type: 'post',
        success: function (data, textStatus, jqXHR) {
            workflowData = data;
            $("#data-request-success").html("Successfully downloaded workflow data.");
            setMetaTable();
            populateDataTable();
            // google.charts.setOnLoadCallback(populateDataTable);
            $('#data-display-button-div').show();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#data-request-error').html("Error downloading workflow data. " + errorThrown);
        },
        complete: function (jqXHR, textStatus) {
            stopLoader();
        }
    });
}

function searchMap() {
    var type = $('#inputLayer').val();
    var searchValue = $('#inputSearch').val();
    if (type === "huc8") {
        if (searchValue.length === 8 && !isNaN(searchValue)) {
            selectHUCs([searchValue]);
        }
    }
}

function startup() {
    $('#startup-div').fadeOut("slow");
}

function populateDataTable() {
    var data = new google.visualization.DataTable();
    data.addColumn('date', 'Date');
    data.addColumn('number', 'Catchment Total Flow');
    //var columns = workflowData['data'][Object.keys(workflowData['data'])[0]].length;
    $.each(workflowData['data'], function (index, row) {
        var r = [];
        var dt = index.split(' ');
        var d = dt[0].split("-");
        var date = new Date(d[0], d[1]-1, d[2]);
        date.setHours(dt[1], 0, 0);
        r.push(date);
        $.each(row, function (key, value) {
            r.push(parseFloat(value));
        });
        data.addRow(r);
    });
    var table = new google.visualization.Table(document.getElementById('data-table'));
    datatableData = data;
    table.draw(data, {allowHtml: true, showRowNumber: false, width: '100%', height: '100%', page: 'enable'});
}

function showData() {
    $('#data-display').fadeIn(300);
}

function closeData() {
    $('#data-display').fadeOut(300);
}

function setMetaTable() {
    var metaTable = new google.visualization.DataTable();
    metaTable.addColumn('string', 'MetaData');
    metaTable.addColumn('string', 'Value');
    $.each(workflowData['metadata'], function (key, value) {
        metaTable.addRow([key, value]);
    });
    var table = new google.visualization.Table(document.getElementById('metadata-table'));
    dataTableMetadata = metaTable;
    table.draw(metaTable, {allowHtml: true, showRowNumber: false, width: '100%', height: '100%', page: 'enable'});
}

function downloadDataAsCSV() {
    var csvData = google.visualization.dataTableToCsv(datatableData);
    var element = document.createElement('a');
    element.setAttribute('href', 'data:application/csv;charset=utf-8,' + encodeURIComponent(csvData));
    element.setAttribute('download', 'workflow-data.csv');
    element.setAttribute('target', '_blank');
    element.style.display = 'none';
    element.click();
}

$(function () {
    setAccordion();
    setDatePickers();
    $('.date-input').on("change", validateDates);
    $('#dataset-input').on("change", validateDataset);
    $('#source-input').on("change", validateSource);
    $('#inputSearch').on("keyup", searchMap);

    setTimeout(startup, 1200);
});
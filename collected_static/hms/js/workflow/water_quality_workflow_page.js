var baseUrl = "/hms/rest/api/v3/workflow/waterquality/";

var taskIDList = null;
var aquatoxTaskIDList = null;
var catchmentList = null;
var currentData = null;
var comidData = {};
var taskID = null;
var counter = 1000;
var requestData = null;
var catchmentMap;
var catchmentGeometry;
var catchmentLayerGroup = null;
var comidTable = null;
var comidDataTable = null;
var selectedCOMID = null;
var timeseriesTable = null;
var timeseriesDataTable = null;
var timeseriesData = null;
var timeseriesGraph = null;
var contributingCatchments = null;
var contributingCatchmentGeometries = null;
var timeseriesColumns = null;
var zipFile = null;
var fileCount = 0;
var aquatoxFileCount = 0;

google.charts.load('current', {'packages': ['table', 'line']});

$(function () {
    $('#catchmentDetails').tabs({
        disabled: [1, 2]
    });
    $('#source_select').selectmenu();
    $('#input_submit_button').button();
    $('#input_submit_button').click(function () {
        setTimeout(getData, 300);
    });
    $('#taskID_submit_button').button();
    $('#taskID_submit_button').click(function () {
        setTimeout(function () {
            taskID = null;
            taskID = $('#input_taskID').val();
            toggleLoader(false, "Processing data request. Task ID: " + taskID);
            $('#catchmentDetails').tabs("enable", 1);
            $('#catchmentDetails').tabs("option", "active", 1);
            setTimeout(getDataPolling, 300);
        }, 300);
    });
    $('#catchment_download').button();
    $('#catchment_download').click(function () {
        setTimeout(downloadCurrentCOMIDData, 300);
    });
    // $('#aoi_download').button();
    $('#aoi_download').click(function () {
        setTimeout(downloadAllCOMIDData, 300);
    });
    $('#previous_tasks_list').click(function (e) {
        console.log(e.currentTarget.innerText);
        $('#catchmentDetails').tabs("enable", 1);
        $('#catchmentDetails').tabs("option", "active", 1);
        toggleLoader(false, "Processing data request. Task ID: " + taskID);
    });

    catchmentMap = L.map('mapid').setView([37.7614, -122.3911], 12);
    setTimeout(function () {
        L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
        }).addTo(catchmentMap);
    }, 300);
    setTimeout(function(){
        var aoiStyle = {
            "color": "#A0FF92",
            "weight": 1,
            "opacity": 0.50
        };
        var geo = L.geoJSON(aoiJSON, {style: aoiStyle});
        geo.addTo(catchmentMap);
    }, 300);

    setTimeout(loadCookies, 400);

    var progressTimer,
        progressbar = $("#progressbar"),
        progressLabel = $(".progress-label"),
        dialogButtons = [{
            text: "Cancel Download",
            click: closeDownload
        }],
        dialog = $("#dialog").dialog({
            autoOpen: false,
            closeOnEscape: false,
            resizable: false,
            buttons: dialogButtons,
            open: function () {
                progressTimer = setTimeout(progress, 2000);
            },
            beforeClose: function () {
                downloadButton.button("option", {
                    disabled: false,
                    label: "Download All Data (CSV)"
                });
            }
        }),
        downloadButton = $("#aoi_download")
            .button()
            .on("click", function () {
                setTimeout(downloadAllCOMIDData, 100);
                $(this).button("option", {
                    disabled: true,
                    label: "Downloading..."
                });
                dialog.dialog("open");
            });

    progressbar.progressbar({
        value: false,
        change: function () {
            progressLabel.text("Current Progress: " + progressbar.progressbar("value") + "%");
        },
        complete: function () {
            progressLabel.text("Complete!");
            dialog.dialog("option", "buttons", [{
                text: "Close",
                click: closeDownload
            }]);
            $(".ui-dialog button").last().trigger("focus");
        }
    });

    function progress() {
        var val = progressbar.progressbar("value") || 0;
        var newVal = Math.round(
            ((fileCount / catchmentList.length) * 40) +
            ((Object.keys(comidData).length / catchmentList.length) * 30) +
            (aquatoxFileCount / aquatoxTaskIDList.length) * 30);

        progressbar.progressbar("value", newVal);

        if (val <= 99) {
            progressTimer = setTimeout(progress, 50);
        } else {
            var zipFileName = "hms-wq-data.zip";
            zipFile.generateAsync({type: "blob"}).then(function (blob) {
                saveAs(blob, zipFileName);
            });
            fileCount = 0;
            aquatoxFileCount = 0;
        }
    }

    function closeDownload() {
        clearTimeout(progressTimer);
        dialog
            .dialog("option", "buttons", dialogButtons)
            .dialog("close");
        progressbar.progressbar("value", false);
        progressLabel
            .text("Starting download...");
        downloadButton.trigger("focus");
    }

});

function setOutputUI() {
    if (catchmentLayerGroup !== null) {
        catchmentMap.removeLayer(catchmentLayerGroup);
        catchmentLayerGroup = null;
    }
    $('#dataset').html("Dataset: " + requestData["dataset"]);
    $('#source').html("Data source: " + requestData["dataSource"]);
    $('#startDate').html("Start Date: " + requestData["metadata"]["startDate"]);
    $('#endDate').html("End Date: " + requestData["metadata"]["endDate"]);

    setOutput();
    getCatchmentsGeometry();
    drawCatchmentTable();
    return false;
}

function getParameters() {
    var requestJson = {
        "dataSource": $('#source_select').val(),
        "minAmmonia": $('#minAmmonia').val(),
        "maxAmmonia": $('#maxAmmonia').val(),
        "minNitrate": $('#minNitrate').val(),
        "maxNitrate": $('#maxNitrate').val()
    };
    return requestJson;
}

function getData() {
    var params = getParameters();
    $.ajax({
        type: "POST",
        url: baseUrl,
        accepts: "application/json",
        data: JSON.stringify(params),
        processData: false,
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            taskID = data.job_id;
            console.log("Data request success. Task ID: " + taskID);
            toggleLoader(false, "Processing data request. Task ID: " + taskID);
            $('#catchmentDetails').tabs("enable", 1);
            $('#catchmentDetails').tabs("option", "active", 1);
            setTimeout(getDataPolling, 12000);
            setDataRequestCookie(taskID);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Data request error...");
            console.log(errorThrown);
            toggleLoader(true, "");
        },
        complete: function (jqXHR, textStatus) {
            console.log("Data request complete");
        }
    });
    return false;
}

function getCatchmentsGeometry() {
    var catchment_base_url = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/Catchments_NP21_Simplified/MapServer/0/query?where=";
    var catchment_url_options = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=%7B%22wkt%22+%3A+%22GEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2C+SPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0%5D%2C+UNIT%5B%5C%22Degree%5C%22%2C0.017453292519943295%5D%5D%22%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    var query = "FEATUREID+IN+(";
    query += catchmentList.join() + ")";
    var query_url = catchment_base_url + query + catchment_url_options;

    $.ajax({
        type: "GET",
        url: query_url,
        success: function (data, textStatus, jqXHR) {
            catchmentGeometry = JSON.parse(data);
            console.log("Catchment data loaded.");
            setOutputMap();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Failed to get catchment data.");
        },
        complete: function (jqXHR, textStatus) {
            console.log(query_url);
            setTimeout(function () {
                toggleLoader(true, "");
            }, 100);
        }
    });
}

function setOutputMap() {
    catchmentLayerGroup = L.featureGroup();
    // catchmentMapList = {};
    $.each(catchmentGeometry.features, function (index, value) {
        var geo = L.geoJSON(value, {
            style: function (feature) {
                return {
                    color: '#B0C0FF',
                    weight: 1,
                    fill: '#C7FFD2'
                };
            }
        });
        // catchmentMapList[value.properties.FEATUREID] = geo._leaflet_id;
        catchmentLayerGroup.addLayer(geo);
    });
    catchmentMap.addLayer(catchmentLayerGroup);
    catchmentMap.fitBounds(catchmentLayerGroup.getBounds());
    catchmentMap.setMaxBounds(catchmentLayerGroup.getBounds());
    // catchmentLayerGroup.on("click", mapClickEvent);
}

function getDataPolling() {
    var requestUrl = "hms/rest/api/v2/hms/data";
    $.ajax({
        type: "GET",
        url: requestUrl + "?job_id=" + taskID,
        accepts: "application/json",
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            if (data.status === "SUCCESS") {
                requestData = data.data;
                console.log("Task successfully completed and data was retrieved.");
                setOutputUI();
                $('#catchmentDetails').tabs("enable", 2);
                toggleLoader(true, "");
            } else if (data.status === "FAILURE") {
                toggleLoader(false, "Task " + taskID + " encountered an error.");
                console.log("Task failed to complete.");
            } else {
                setTimeout(getDataPolling, 12000);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Data request error...");
            console.log(errorThrown);
            toggleLoader(false, "Error retrieving data for task ID: " + taskID);
        },
        complete: function (jqXHR, textStatus) {
            console.log("Data request complete");
        }
    });
    return false;
}

function toggleLoader(hide, msg) {
    if (hide) {
        $("#loader").fadeOut(100);
        $("#loader_message").html();
    } else {
        $("#loader").fadeIn(100);
        $("#loader_message").html("<span>" + msg + "</span>");
    }
    return false;
}

function setOutput() {
    if (requestData !== null) {
        taskIDList = [];
        Object.entries(requestData['data']['taskIDs']).forEach(([index, value]) => {
            taskIDList.push(value);
        });
        aquatoxTaskIDList = [];
        Object.entries(requestData['data']['aquatoxTaskIDs']).forEach(([index, value]) => {
            aquatoxTaskIDList.push(value);
        });
        catchmentList = [];
        Object.entries(taskIDList).forEach(([index, value]) => {
            var taskIDComp = value.split("-");
            catchmentList.push(Number.parseFloat(taskIDComp[taskIDComp.length - 1]));
        });
    }
}

function drawCatchmentTable() {
    comidDataTable = new google.visualization.DataTable();
    comidDataTable.addColumn('string', 'COMID');
    comidDataTable.addColumn('string', 'Task ID');
    Object.entries(catchmentList).forEach(([index, value]) => {
        comidDataTable.addRow([value.toString(), taskIDList[index]]);
    });
    comidTable = new google.visualization.Table(document.getElementById('catchmentTable'));
    var tableOptions = {
        pageSize: 15,
        width: '100%',
        height: '100%'
    };
    comidTable.draw(comidDataTable, tableOptions);
    google.visualization.events.addListener(comidTable, 'select', getDataByCOMID);
    return false;
}

function getDataByCOMID() {
    selectedCOMID = comidDataTable.getFormattedValue(comidTable.getSelection()[0].row, 0);
    if (selectedCOMID in comidData) {
        currentData = comidData[selectedCOMID];
        setTimeout(setTimeSeriesData, 300);
        setTimeout(showContributingCatchments, 300);
    } else {
        var selectedTaskID = comidDataTable.getFormattedValue(comidTable.getSelection()[0].row, 1);
        var requestUrl = "hms/rest/api/v2/hms/data";
        $.ajax({
            type: "GET",
            url: requestUrl + "?job_id=" + selectedTaskID,
            accepts: "application/json",
            timeout: 0,
            contentType: "application/json",
            success: function (data, textStatus, jqXHR) {
                currentData = data.data;
                comidData[selectedCOMID] = data.data;
                setTimeout(setTimeSeriesData, 300);
                setTimeout(showContributingCatchments, 300);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }
}

function getDataBySingleCOMID(comid, tID) {
    if (comid in comidData) {
        buildDataTable(comid, comidData[selectedCOMID]);
    } else {
        var requestUrl = "hms/rest/api/v2/hms/data";
        $.ajax({
            type: "GET",
            url: requestUrl + "?job_id=" + tID,
            accepts: "application/json",
            timeout: 0,
            contentType: "application/json",
            success: function (data, textStatus, jqXHR) {
                comidData[comid] = data.data;
                buildDataTable(comid, data.data);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }
}

function setTimeSeriesData() {
    timeseriesDataTable = new google.visualization.DataTable();
    timeseriesColumns = [];
    timeseriesColumns.push('date');
    timeseriesDataTable.addColumn('string', 'date');
    for (var i = 1; i < currentData.Data[requestData.metadata.startDate + " 00"].length + 1; i++) {
        var key = "wq_workflow_column_" + i;
        if (key in currentData.Metadata) {
            timeseriesDataTable.addColumn('number', currentData.Metadata[key].toString());
            timeseriesColumns.push(currentData.Metadata[key].toString());
        } else {
            timeseriesDataTable.addColumn('number', "undefined_" + i);
            timeseriesColumns.push("undefined_" + i);
        }
    }
    timeseriesData = [];
    Object.entries(currentData.Data).forEach(([key, value]) => {
        var row = [];
        row.push(key);
        Object.entries(value).forEach(([i, d]) => {
            row.push(parseFloat(d));
        });
        timeseriesData.push(row);
    });
    timeseriesDataTable.addRows(timeseriesData);
    timeseriesTable = new google.visualization.Table(document.getElementById('timeseriesTable'));
    var tableOptions = {
        page: 'enable'
    };
    timeseriesTable.draw(timeseriesDataTable, tableOptions);

    return false;
}

function showContributingCatchments() {
    var catchment_base_url = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/Catchments_NP21_Simplified/MapServer/0/query?where=";
    var catchment_url_options = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=%7B%22wkt%22+%3A+%22GEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2C+SPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0%5D%2C+UNIT%5B%5C%22Degree%5C%22%2C0.017453292519943295%5D%5D%22%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    var query = "FEATUREID+IN+(";
    query += currentData.Metadata["wq_workflow_ContributingCOMIDs"] + ")";
    var query_url = catchment_base_url + query + catchment_url_options;
    $.ajax({
        type: "GET",
        url: query_url,
        success: function (data, textStatus, jqXHR) {
            contributingCatchmentGeometries = JSON.parse(data);
            console.log("Catchment data loaded.");
            setTimeout(addContributing, 300);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log("Failed to get catchment data.");
        }
    });
}

function addContributing() {
    if (contributingCatchments !== null) {
        catchmentMap.removeLayer(contributingCatchments);
        contributingCatchments = null;
    }
    contributingCatchments = L.featureGroup();
    $.each(contributingCatchmentGeometries.features, function (index, value) {
        var geo = L.geoJSON(value, {
            style: function (feature) {
                return {
                    color: '#E8DE3F',
                    weight: 1,
                    fill: '#C7FFD2'
                };
            }
        });
        contributingCatchments.addLayer(geo);
    });
    catchmentMap.addLayer(contributingCatchments);
}

function downloadCurrentCOMIDData() {
    if (selectedCOMID !== null) {
        var csvFormattedDataTable = timeseriesColumns.join(",") + "\n" + google.visualization.dataTableToCsv(timeseriesDataTable);
        var encodedUri = 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(csvFormattedDataTable);
        var filename = 'hms-wq-data-' + selectedCOMID;
        var pom = document.createElement('a');
        pom.setAttribute('href', encodedUri);
        pom.setAttribute('download', filename + '.csv');
        if (document.createEvent) {
            var event = document.createEvent('MouseEvents');
            event.initEvent('click', true, true);
            pom.dispatchEvent(event);
        } else {
            pom.click();
        }
    }
}

function downloadAllCOMIDData() {
    zipFile = new JSZip();
    var jsonData = JSON.stringify(requestData);
    var filename = 'hms-wq-data-request-data.json';
    zipFile.file(filename, jsonData);
    Object.entries(catchmentList).forEach(([index, comid]) => {
        if (comid === selectedCOMID) {
            writeCSV(comid, timeseriesDataTable);
        } else if (comid in comidData) {
            buildDataTable(comid, comidData[comid]);
        } else {
            var taskID = taskIDList[parseInt(index)];
            getDataBySingleCOMID(comid, taskID);
        }
    });
    Object.entries(aquatoxTaskIDList).forEach(([index, taskID]) => {
        var comid = catchmentList[index];
        requestDataByTaskID(comid, taskID);
    });
}

function buildDataTable(comid, data) {
    var dt = new google.visualization.DataTable();
    dt.addColumn('string', 'Date');
    timeseriesColumns = [];
    timeseriesColumns.push('date');
    for (var i = 1; i < data.Data[requestData.metadata.startDate + " 00"].length + 1; i++) {
        var key = "wq_workflow_column_" + i;
        if (key in data.Metadata) {
            dt.addColumn('number', data.Metadata[key].toString());
            timeseriesColumns.push(data.Metadata[key].toString());
        } else {
            dt.addColumn('number', "undefined_" + i);
            timeseriesColumns.push("undefined_" + i);
        }
    }
    var tsD = [];
    Object.entries(data.Data).forEach(([key, value]) => {
        var row = [];
        row.push(key);
        Object.entries(value).forEach(([i, d]) => {
            row.push(parseFloat(d));
        });
        tsD.push(row);
    });
    dt.addRows(tsD);
    writeCSV(comid, dt, data);
}

function writeJSON(comid, data) {
    var jsonData = JSON.stringify(data);
    var filename = 'hms-wq-data-' + comid + '-aquatox.json';
    zipFile.file(filename, jsonData);
    aquatoxFileCount += 1;
}

function writeCSV(comid, dt, data) {
    var csvFormattedDataTable = timeseriesColumns.join(",") + "\n" + google.visualization.dataTableToCsv(dt);
    var filename = 'hms-wq-data-' + comid + '.csv';
    zipFile.file(filename, csvFormattedDataTable);
    var jsonData = JSON.stringify(data);
    var jsonFilename = 'hms-wq-data-' + comid+ '.json';
    zipFile.file(jsonFilename, jsonData);
    fileCount += 1;
}

function setDataRequestCookie(taskID) {
    var daysToExpire = 1;
    var date = new Date();
    date.setTime(date.getTime() + daysToExpire * 24 * 60 * 60 * 1000);
    var expires = "expires=" + date.toUTCString();
    var url = window.location.href;
    var current = getCookie(url);
    var taskIDs = taskID + "," + current;
    document.cookie = url + "=" + taskIDs + ";" + expires + ";path/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function loadCookies() {
    var url = window.location.href;
    var cookie = getCookie(url);
    var ids = cookie.split(",");
    if (ids.length > 1) {
        $("#previous_tasks").show();
        var list = $('#previous_tasks_list')[0];
        ids.forEach(function (id) {
            if (id !== "") {
                var ele = document.createElement("li");
                ele.innerText = id;
                ele.onclick = function () {
                    taskID = id;
                    setTimeout(getDataPolling, 300);
                };
                list.appendChild(ele);
            }
        });
    }
}

function requestDataByTaskID(comid, tID) {
    var requestUrl = "hms/rest/api/v2/hms/data";
    $.ajax({
        type: "GET",
        url: requestUrl + "?job_id=" + tID,
        accepts: "application/json",
        timeout: 0,
        contentType: "application/json",
        success: function (data, textStatus, jqXHR) {
            writeJSON(comid, data.data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

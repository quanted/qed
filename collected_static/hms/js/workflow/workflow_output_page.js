var jobData = null;
var jobID = null;
var taskID = null;
var catchmentData = null;
var catchmentInfo = null;
var catchmentMap = null;
var catchmentMapList = {};
var geoGroup = null;
var dyGraph = null;
var catchmentListTable = null;
var catchmentInfoTable = null;
var catchmentDataTable = null;
var selectedRow = null;
var selectedCatchment = null;


function setOutputUI()
{
    setOutputPage();
}

function setOutputTitle() {
    if (taskID === null && testData) {
        taskID = "TESTTASK1234567890";
    }
    var title = "Data for Workflow job: " + taskID.toString();
    var output_title = $("#output_title");
    output_title.html("<h3>" + title + "</h3>");
}

function getCatchmentData() {
    var catchment_base_url = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/Catchments_NP21_Simplified/MapServer/0/query?where=";
    var catchment_url_options = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=%7B%22wkt%22+%3A+%22GEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2C+SPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0%5D%2C+UNIT%5B%5C%22Degree%5C%22%2C0.017453292519943295%5D%5D%22%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    var n = 1;
    var query = "FEATUREID+IN+(";
    var catchments = jobData.metadata.catchments;//.split(',');
    query += catchments + ")";
    var query_url = catchment_base_url + query + catchment_url_options;

    $.ajax({
        type: "GET",
        url: query_url,
        success: function (data, textStatus, jqXHR) {
            if (typeof data === "string") {
                catchmentData = JSON.parse(data);
            }else{
                catchmentData = data;
            }
            console.log("Catchment data loaded.");
            setOutputTitle();
            setOutputMap();
            setOutputComidList();
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

function catchmentTableToggle(comid, select) {
    let selectOption = "selectRow";
    if (!select) {
        selectOption = "deselectRow";
    }
    let rows = $('#output_comid_list').tabulator("getData");
    let row = 0;
    let i = 0;
    $.each(rows, function (v) {
        if (rows[v].id === comid) {
            row = i;
        }
        i += 1;
    });
    console.log(row + " " + rows[row].id);
    $('#output_comid_list').tabulator(selectOption, rows[row].id);
    if (select) {
        $('#output_comid_list').tabulator("scrollToRow", rows[row].id);
    }
}

function mapClickEvent(e) {
    let comid = e.sourceTarget.feature.properties.FEATUREID;
    if (selectedRow === null || selectedRow !== comid) {
        if (selectedCatchment !== null) {
            selectCatchmentOnMap(selectedCatchment, false);
        }
        catchmentTableToggle(comid, true);
        toggleLoader(false, "Loading data for Catchment: " + comid);
        setTimeout(function () {
            showCatchmentDetails(true);
            selectedRow = comid;
            selectComid(comid);
            selectCatchmentOnMap(comid, true);
            setTimeout(function () {
                toggleLoader(true, "");
            }, 60);
        }, 300);
    }
    else {
        catchmentTableToggle(selectedCatchment, false);
        selectCatchmentOnMap(selectedCatchment, false);
        showCatchmentDetails(false);
        selectedRow = null;
    }
}

function setOutputMap() {
    if (catchmentMap === null) {
        catchmentMap = L.map("output_map");
        L.esri.basemapLayer('Topographic').addTo(catchmentMap);
    }
    geoGroup = L.featureGroup();
    catchmentMapList = {};
    $.each(catchmentData.features, function (index, value) {
        var geo = L.geoJSON(value, {
            style: function (feature) {
                return {
                    color: '#964AFF',
                    weight: 1,
                    fill: '#5238E8'
                };
            }
        });
        catchmentMapList[value.properties.FEATUREID] = geo._leaflet_id;
        geoGroup.addLayer(geo);
    });
    catchmentMap.addLayer(geoGroup);
    catchmentMap.fitBounds(geoGroup.getBounds());
    catchmentMap.setMaxBounds(geoGroup.getBounds());
    geoGroup.on("click", mapClickEvent);
}

function setOutputComidList() {
    var data = [];
    $.each(catchmentData.features, function (index, value) {
        var d = {
            id: value.properties.FEATUREID,
            // region: value.properties.NHDPLUS_REGION,
            huc12: value.properties.WBD_HUC12,
            area: Number.parseFloat(value.properties.AREASQKM).toFixed(4)
        };
        data.push(d);
    });

    if (catchmentListTable) {
        $('#output_comid_list').tabulator("destroy");
        catchmentListTable = null;
    }
    catchmentListTable = true;
    $("#output_comid_list").tabulator({
        layout: "fitColumns",
        selectable: 1,
        height: 250,
        rowClick: function (e, row) {
            var d = row.getData();
            if (selectedRow === null || selectedRow !== d.id) {
                if (selectedCatchment !== null) {
                    selectCatchmentOnMap(selectedCatchment, false);
                }
                toggleLoader(false, "Loading data for Catchment: " + d.id);
                setTimeout(function () {
                    showCatchmentDetails(true);
                    selectedRow = d.id;
                    selectComid(d.id);
                    selectCatchmentOnMap(d.id, true);
                    setTimeout(function () {
                        toggleLoader(true, "");
                    }, 60);
                }, 300);
            }
            else {
                selectCatchmentOnMap(selectedCatchment, false);
                showCatchmentDetails(false);
                selectedRow = null;
            }
            return false;
        },
        initialSort: [{column: 'id', dir: "asc"}],
        columns: [
            {title: "Catchment ID", field: "id", align: "left", sorter: "number"},
            // {title: "Region", field: "region", align: "left", headerSort: false},
            {title: "HUC 12", field: "huc12", align: "left", headerSort: false},
            {title: "Area (km&#178)", field: "area", align: "left", headerSort: false},
        ],
        data: data
    });
}

function setInfoDiv(comid) {
    let title = "Stream: " + comid.toString() + " Details";
    $('#output_info h4').html(title);
    let data = {};
    $.each(jobData.table[comid], function (k, v) {
        let val = parseFloat(v);
        if (isNaN(val)) {
            val = v;
        }
        else{
            val = val.toFixed(4);
        }
        data[k] = val;
    });
    if (catchmentInfoTable) {
        $('#output_info_div').tabulator("destroy");
        catchmentInfoTable = null;
    }
    catchmentInfoTable = true;
    $("#output_info_div").tabulator({
        layout: "fitColumns",
        selectable: false,
        columns: [
            {title: "From ComID", field: "FROMCOMID", align: "left", headerSort: false},
            {title: "To ComID", field: "TOCOMID", align: "left", headerSort: false},
            {title: "Slope", field: "SLOPE", align: "left", headerSort: false},
            {title: "Length (km)", field: "LengthKM", align: "left", headerSort: false},
            {title: "Stream Level", field: "StreamLeve", align: "left", headerSort: false},
            {title: "Stream Order", field: "StreamOrde", align: "left", headerSort: false},
            {title: "Mean Annual Flow (m&#178/s)", field: "MeanAnnFlowM3PS", align: "left", headerSort: false},
            {title: "Mean Annual Velocity (m/s)", field: "MeanAnnVelMPS", align: "left", headerSort: false},
        ],
        data: [data]
    });
}

function setOutputGraph(comid) {
    var dataTitle = "Catchment: " + comid + " Data";
    var labels = ["Date", "Precipitation (mm)", "Surface Runoff (mm)", "Subsurface Flow (mm)", "Stream Flow (m^3/s)"];
    var dataCSV = [];
    var dataDict = [];
    var cData = jobData.data[comid];
    var maxValue = 0.0;
    $.each(cData.Precipitation.data, function (index, row) {
        var rowD = [];
        var date;
        if (index.includes("/")) {
            let d = index.split("/");
            date = new Date(d[2], d[0] - 1, d[1], 0, 0, 0);
        }
        else if (index.includes("-")) {
            var dt = index.split(' ');
            var d = dt[0].split('-');
            if (dt.length === 2) {
                var hr = dt[1].split(':');
                if (hr.length === 2) {
                    date = new Date(d[0], d[1] - 1, d[2], hr[0], hr[1], 0, 0);
                }
                else {
                    date = new Date(d[0], d[1] - 1, d[2], dt[1], 0, 0, 0);
                }
            }
            else {
                date = new Date(d[0], d[1] - 1, d[2], 0, 0, 0);
            }
        }
        rowD.push(date);

        var p = Number.parseFloat(row);
        var sr = Number.parseFloat(cData.SurfaceRunoff.data[index]);
        var sbf = Number.parseFloat(cData.SubsurfaceRunoff.data[index]);
        var sf = Number.parseFloat(cData.StreamHydrology.data[index]);

        if(p > maxValue){
            maxValue = p;
        }
        if(sr > maxValue){
            maxValue = sr;
        }
        if(sbf > maxValue){
            maxValue = sbf;
        }
        if(sf > maxValue){
            maxValue = sf;
        }

        rowD.push(p);
        rowD.push(sr);
        rowD.push(sbf);
        rowD.push(sf);

        dataDict.push({
            date: date,
            precip: p,
            runoff: sr,
            subsurfaceflow: sbf,
            streamflow: sf
        });
        dataCSV.push(rowD);
    });
    var graphEle = document.getElementById('output_graph');
    if (dyGraph) {
        dyGraph.destroy();
    }
    var graphOptions = {
        labels: labels,
        rollPeriod: 1,
        showRoller: true,
        valueRange: [-10.0, maxValue + 10.0]
    };
    dyGraph = new Dygraph(graphEle, dataCSV, graphOptions);
    setOutputTable(dataDict);
}

function setOutputTable(data) {
    if (catchmentDataTable) {
        $('#output_table').tabulator("destroy");
        catchmentDataTable = null;
    }
    //custom date formatter
    var dateFormatter = function (cell, formatterParams) {
        var value = cell.getValue();

        if (value) {
            value = moment(value, "YYYY/MM/DD").format("MM/DD/YYYY");
        }

        return value;
    };
    catchmentDataTable = true;
    $('#output_table').tabulator({
        layout: "fitColumns",
        height: "250px",
        columns: [
            {title: "Date", field: "date", align: "left", headerSort: false, formatter: dateFormatter},
            {title: "Precipitation (mm)", field: "precip", align: "left", headerSort: false},
            {title: "Surface Runoff (mm)", field: "runoff", align: "left", headerSort: false},
            {title: "Subsurface Runoff (mm)", field: "subsurfaceflow", align: "left", headerSort: false},
            {title: "Stream Flow (m&#178/s)", field: "streamflow", align: "left", headerSort: false}
        ],
        data: data
    });
}

function errorCheck(){
    if(jobData.metadata.hasOwnProperty("ERROR")){
        toggleLoader(false, jobData.metadata["ERROR"]);
        return false;
    }
    return true;
}

function setOutputPage() {
    //parseData();

    var validData = errorCheck();
    if(validData) {
        setTimeout(function () {
            toggleLoader(false, "Loading task data...");
        }, 60);
        getCatchmentData();
    }
}

function parseData(){
    var table = {};
    $.each(jobData.table, function (comid, v) {
        if (typeof v === "string") {
            table.comid = JSON.parse(v);
        }else{
            table.comid = v;
        }
    });
    jobData.table = table;
    var comidData = {};
    $.each(jobData.data, function(comid, array_v){
        var comidArray = [];
        $.each(array_v, function(k, v){
            if (typeof v === "string") {
                comidArray.push(JSON.parse(v));
            }else{
                comidArray.push(v);
            }
        });
        comidData[comid] = comidArray;
    });
    jobData.data = comidData;
}

function selectComid(comid) {
    selectedCatchment = comid;
    $('#output_center_bottom').tabs();
    $('#output_center_bottom').tabs("option", "active", 0);
    $('#output_center_bottom').tabs({
        activate: function(event, ui){
            var active = $('#output_center_bottom').tabs("option", "active");
            if(active === 1){
                $('#output_table').tabulator("redraw");
            }
        }
    });
    setInfoDiv(comid);
    setOutputGraph(comid);
    dyGraph.resize();
    return false;
}

function selectCatchmentOnMap(comid, selected) {
    if (selected) {
        let l = geoGroup.getLayer(catchmentMapList[comid])
        l.setStyle({
            color: '#33994C',
            weight: 2,
            fill: '#4EE874'
        });
        catchmentMap.fitBounds(l.getBounds());
    }
    else {
        geoGroup.getLayer(catchmentMapList[comid]).setStyle({
            color: '#964AFF',
            weight: 1,
            fill: '#5238E8'
        });
        catchmentMap.fitBounds(geoGroup.getBounds());
    }
}

function showCatchmentDetails(hide) {
    if (hide) {
        $("#output_info").show();
        $("#output_center_bottom").show();
        toggleSaveButtons(false);

    }
    else {
        $("#output_info").hide();
        $("#output_center_bottom").hide();
        toggleSaveButtons(true);
    }
    return false;
}

function toggleLoader(hide, msg) {
    if (hide) {
        $("#output_loading").fadeOut(100);
        $("#loading_msg").html();
    }
    else {
        $("#output_loading").fadeIn(100);
        $("#loading_msg").html("<span>" + msg + "</span>");
    }
    return false;
}

function toggleSaveButtons(hide) {
    if (hide) {
        $('#export_json_catchment').hide();
        $('#export_csv_catchment').hide();
    }
    else {
        $('#export_json_catchment').show();
        $('#export_csv_catchment').show();
    }
    return false;
}

function exportAllDataToCSV() {
    var fileName = "hms_catchment_data_" + taskID + ".csv";
    // var metadata = "";
    var dataRows = [];
    var columns = "Date(GMT),ComID";
    var first = true;
    var firstCOMID = true;
    var i = 0;
    var i_max = 0;
    var i0 = 0;
    // each catchment
    $.each(jobData.data, function (j, u) {
        var comid = j;
        // each dataset
        $.each(u, function (k, v) {
            if(firstCOMID) {
                if (v.metadata["units"]) {
                    columns += "," + k + " (" + v.metadata["units"] + ")";
                } else {
                    columns += "," + k;
                }
            }
            // $.each(v.metadata, function (l, w) {
            //     metadata += j + "," + k + "," + l + "," + w + "\n";
            // });
            if (first) {
                $.each(v.data, function (m, x) {
                    dataRows[i + i0] = m + "," + comid + "," + x;
                    i += 1;
                });
            }
            else {
                $.each(v.data, function (m, x) {
                    dataRows[i + i0] += "," + x;
                    i += 1;
                });
            }
            i_max = i;
            i = 0;
            first = false;
        });
        first = true;
        firstCOMID = false;
        i0 += i_max;
    });

    var metadata = JSON.parse(JSON.stringify(jobData));
    $.each(jobData.data, function (j, u) {
        $.each(u, function (k, v) {
            metadata.data[j][k].data = undefined;
        });
    });
    var metadata_name = "hms_catchment_metadata_" + taskID + ".json";
    exportDataAsJSON(metadata_name, metadata);

    var data = dataRows.join("\n");
    var csvFinal = columns + "\n" + data;// + "\n\nMetadata\n" + metadata;
    var dataStr = 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(csvFinal);
    var pom = document.createElement('a');
    pom.setAttribute('href', dataStr);
    pom.setAttribute('download', fileName);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
    return false;
}

function exportCatchmentDataToCSV() {
    var fileName = "hms_catchment_data_" + selectedCatchment + "_" + taskID + ".csv";
    var dataRows = [];
    var columns = "Date(GMT),ComID";
    var first = true;
    var i = 0;
    $.each(jobData.data[selectedCatchment], function (k, v) {
        if (v.metadata["units"]) {
            columns += "," + k + " (" + v.metadata["units"] + ")";
        } else {
            columns += "," + k;
        }
        // $.each(v.metadata, function (l, w) {
        //     metadata += k + "_" + l + "," + w + "\n";
        // });
        if (first) {
            $.each(v.data, function (m, x) {
                dataRows[i] = m + "," + selectedCatchment + "," + x;
                i += 1;
            });
        } else {
            $.each(v.data, function (m, x) {
                dataRows[i] += "," + x;
                i += 1;
            });
        }
        i = 0;
        first = false;
    });

    var metadata = JSON.parse(JSON.stringify(jobData.data[selectedCatchment]));
    $.each(metadata, function (j, u) {
        metadata[j].data = undefined;
    });
    metadata.data = undefined;
    var metadata_name = "hms_catchment_metadata_" + selectedCatchment + "_" + taskID + ".json";
    exportDataAsJSON(metadata_name, metadata);

    var data = dataRows.join("\n");
    var csvFinal = columns + "\n" + data; // + "\n\nMetadata\n" + metadata;
    var dataStr = 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(csvFinal);
    var pom = document.createElement('a');
    pom.setAttribute('href', dataStr);
    pom.setAttribute('download', fileName);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
    return false;
}

function exportAllDataToJSON() {
    var fileName = "hms_data_" + taskID + ".json";
    var pom = document.createElement('a');
    var data = encodeURIComponent(JSON.stringify(jobData));
    pom.setAttribute('href', 'data:data:text/plain;charset=utf-8,' + data);
    pom.setAttribute('download', fileName);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function exportCatchmentDataToJSON() {
    var fileName = "hms_catchment_data_" + selectedCatchment + "_" + taskID + ".json";
    var d = jobData.data[selectedCatchment];
    var pom = document.createElement('a');
    var data = encodeURIComponent(JSON.stringify(d));
    pom.setAttribute('href', 'data:data:text/plain;charset=utf-8,' + data);
    pom.setAttribute('download', fileName);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

function exportDataAsJSON(name, output){
    var pom = document.createElement('a');
    var data = encodeURIComponent(JSON.stringify(output));
    pom.setAttribute('href', 'data:data:text/plain;charset=utf-8,' + data);
    pom.setAttribute('download', name);
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}

var baseUrl = "/hms/rest/api/v3/workflow/watershed/";
var inputJSON = {};
var requiredInputs = ["spatialType", "spatialInput", "startDate", "endDate", "timestep", "runoffSource", "precipSource", "streamAlgorithm"];
var hucMap = null;
var counter = 100;
var testData = false;

$(function () {
    pageLoadStart();

    // Workflow Inputs Tab events //
    var datepicker_options = {
        changeMonth: true,
        changeYear: true,
        autosize: true,
        yearRange: '1900:2100'
    };
    // Page load functions
    $("#start_datepicker").datepicker(datepicker_options);
    $("#end_datepicker").datepicker(datepicker_options);

    // setTimeout(loadCookies, 400);

    // Input window actions
    $("#spatial_input_button").click(toggleSpatialInputs);
    $("#temporal_input_button").click(toggleTemporalInputs);
    $("#runoff_algorithm_input_button").click(toggleRunoffInputs);
    $("#precip_source_input_button").click(togglePrecipInputs);
    $("#stream_algorithm_input_button").click(toggleStreamInputs);

    // Input Validation actions
    $("#huc_id").change(spatialInputValidation);
    $('#comid').change(spatialInputValidation);
    $("#spatial_type").change(spatialInputValidation);
});

function pageLoadStart() {
    // $('#load_page').fadeOut(600);
    // $("#workflow_tabs").tabs({
    //     active: 0,
    //     disabled: [2]
    // });
    browserCheck();
    return false;
}

// Workflow Inputs Tab Functions //
function setErrorMessage(errorMsg, remove) {
    var errorMsgBlock = document.getElementById("notifications");
    if (remove) {
        errorMsgBlock.innerText = "";
    } else {
        errorMsgBlock.innerHTML = errorMsg;
    }
    return false;
}

function toggleOffAllInputs() {
    $(".workflow_input").removeClass("selected");
    $('.input_fields').fadeOut("faster");
    setErrorMessage("", true);
    return false;
}

function toggleInputField(button, inputBlock) {
    var active = false;
    if (button.hasClass("selected")) {
        active = true;
    }
    toggleOffAllInputs();
    if (!active) {
        button.addClass("selected");
        inputBlock.fadeIn("faster", "linear").css("display", "inline-block");
    }
    return false;
}

function spatialInputValidation() {
    var selectedType = $("#spatial_type").val();
    if (selectedType === "hucid") {
        var hucid = $("#huc_id").val();
        if (Number.isInteger(Number(hucid)) && hucid.length === 12) {
            $('#add_spatial_input').removeClass("blocked");
        }
        else {
            if ($('#add_spatial_input').hasClass("blocked")) {
            }
            else {
                $('#add_spatial_input').addClass("blocked");
            }
        }
        $("#huc_id").focus();
    }
    else if (selectedType === "comid") {
        var comid = $('#comid').val();
        if (Number.isInteger(Number(comid)) && comid.length >= 6) {
            $('#add_spatial_input').removeClass("blocked");
        }
        else {
            if ($('#add_spatial_input').hasClass("blocked")) {
            }
            else {
                $('#add_spatial_input').addClass("blocked");
            }
        }
        $("#comid").focus();
    }
    else {
        if (!$('#add_spatial_input').hasClass("blocked")) {
            $('#add_spatial_input').addClass("blocked");
        }
    }
    return false;
}

function dateValidation(startDate, endDate) {
    startDate = startDate.getTime();
    endDate = endDate.getTime();
    if (startDate > endDate) {
        setErrorMessage("Opps! The start date must be a date before or the same as the end date.", false);
        return false;
    }
    return true;
}

function spatialTypeSelect() {
    $('#spatial_type_huc').hide();
    $('#spatial_type_comid').hide();
    var selection = $("#spatial_type").val();
    if (selection === "hucid") {
        $('#spatial_type_huc').show();
    }
    else if (selection === "comid") {
        $('#spatial_type_comid').show();
    }
    else {
        $('#spatial_type_huc').show();
    }
    return false;
}

function validateInput() {
    var valid = true;
    requiredInputs.map(function (input) {
        if (!inputJSON.hasOwnProperty(input)) {
            valid = false;
        }
    });
    return valid;
}

function toggleSpatialInputs() {
    var spatialButton = $("#spatial_input_button");
    var spatialBlock = $("#spatial_input");
    toggleInputField(spatialButton, spatialBlock);
    return false;
}

function toggleTemporalInputs() {
    var temporalButton = $('#temporal_input_button');
    var temporalBlock = $('#temporal_input');
    toggleInputField(temporalButton, temporalBlock);
    return false;
}

function toggleRunoffInputs() {
    var runoffButton = $('#runoff_algorithm_input_button');
    var runoffBlock = $('#runoff_input');
    toggleInputField(runoffButton, runoffBlock);
    return false;
}

function togglePrecipInputs() {
    var precipButton = $('#precip_source_input_button');
    var precipBlock = $('#precip_input');
    if (precipButton.hasClass("blocked")) {
        return false;
    }
    toggleInputField(precipButton, precipBlock);
    return false;
}

function toggleStreamInputs() {
    var streamButton = $('#stream_algorithm_input_button');
    var streamBlock = $('#stream_input');
    toggleInputField(streamButton, streamBlock);
    return false;
}

function addToInputTable(row, key, value) {
    var inputKey = document.createElement("div");
    inputKey.setAttribute("class", "input_column_0");
    inputKey.innerHTML = key;
    var inputValue = document.createElement("div");
    inputValue.setAttribute("class", "input_column_1");
    inputValue.innerHTML = value;
    $(row).empty();
    row.appendChild(inputKey);
    row.appendChild(inputValue);
    if (validateInput()) {
        $('#submit_workflow').removeClass("blocked");
    }
    else {
        if (!$('#submit_workflow').hasClass("blocked")) {
            $('#submit_workflow').addClass("blocked");
        }
    }
    return false;
}

function addSpatialInput() {
    if ($('#add_spatial_input').hasClass("blocked")) {
        return false;
    }
    var selectedType = $("#spatial_type").val();
    var id = "";
    if (selectedType === "hucid") {
        id = $("#huc_id").val();
    }
    else {
        id = $("#comid").val();
    }
    inputJSON.spatialType = selectedType;
    inputJSON.spatialInput = id;
    var row = document.getElementById("selected_spatial_input");
    addToInputTable(row, selectedType, id);
    console.log(inputJSON);
    setErrorMessage("", true);
    $('#add_spatial_input').text("Update");
    $('#add_spatial_input').attr("title", "Update selected spatial input.");
    return false;
}

function addTemporalInput() {
    var startDate = $("#start_datepicker").val();
    var endDate = $("#end_datepicker").val();
    var timestep = $("#timestep option:selected").val();
    setErrorMessage("", true);
    if (!dateValidation(new Date(startDate), new Date(endDate))) {
        return false;
    }
    inputJSON.startDate = startDate;
    inputJSON.endDate = endDate;
    inputJSON.timestep = timestep;
    var row1 = document.getElementById("selected_startdate_input");
    var row2 = document.getElementById("selected_enddate_input");
    var row3 = document.getElementById("selected_timestep_input");
    addToInputTable(row1, "startDate", startDate);
    addToInputTable(row2, "endDate", endDate);
    addToInputTable(row3, "timestep", timestep);
    console.log(inputJSON);
    $('#add_temporal_input').text("Update");
    $('#add_temporal_input').attr("title", "Update selected date/time inputs.");
    return false;
}

function addRunoffInput() {
    var runoffSelected = $("#runoff_select").val();
    setErrorMessage("", true);
    inputJSON.runoffSource = runoffSelected;
    var row = document.getElementById("selected_runoff_input");
    addToInputTable(row, "runoffSource", runoffSelected);
    if (runoffSelected === "curvenumber") {
        $("#precip_source_input_button").removeClass("blocked");
    }
    else {
        inputJSON.precipSource = "NULL";
        $("#precip_source_input_button").addClass("blocked");
        addToInputTable($('#selected_precip_input'), "", "");
    }
    console.log(inputJSON);
    $("#add_runoff_input").text("Update");
    $('#add_runoff_input').attr("title", "Update selected runoff input.");
    return false;
}

function addPrecipInput() {
    var precipSelected = $("#precip_select").val();
    setErrorMessage("", true);
    inputJSON.precipSource = precipSelected;
    var row = document.getElementById("selected_precip_input");
    addToInputTable(row, "precipSource", precipSelected);
    console.log(inputJSON);
    $('#add_precip_input').text("Update");
    $('#add_precip_input').attr("title", "Update selected precipitation input.");
    return false;
}

function addStreamInput() {
    var streamSelected = $("#stream_algorithm_select").val();
    setErrorMessage("", true);
    inputJSON.streamAlgorithm = streamSelected;
    var row = document.getElementById("selected_stream_input");
    addToInputTable(row, "streamAlgorithm", streamSelected);
    console.log(inputJSON);
    $("#add_stream_input").text("Update");
    $('#add_stream_input').attr("title", "Update selected stream algorithm input.");
    return false;
}

function submitWorkflowJob() {
    if ($('#submit_workflow').hasClass("blocked")) {
        return false;
    }
    if (testData) {
        jobData = test_data;
        setOutputPage();
        $('#workflow_tabs').tabs("enable", 2);
        $('#workflow_tabs').tabs("option", "active", 2);
        return false;
    }
    else {
        getData();
    }
}

function getParameters() {
    // Dataset specific request object
    let precip = "";
    if (inputJSON.precipSource === "NULL") {
        precip = "daymet";
    }
    else {
        precip = inputJSON.precipSource;
    }
    var requestJson = {
        "source": "streamflow",
        "aggregation": false,
        "runoffsource": inputJSON.runoffSource,
        "streamhydrology": inputJSON.streamAlgorithm,
        "datetimespan": {
            "startdate": inputJSON.startDate,
            "enddate": inputJSON.endDate,
        },
        "geometry": {
        },
        "temporalresolution": inputJSON.timestep,
        "outputformat": "json"
    };
    if (inputJSON.spatialType === "hucid") {
        requestJson.geometry["hucID"] = inputJSON.spatialInput;
    }
    else {
        requestJson.geometry["comID"] = inputJSON.spatialInput;
    }
    if (requestJson.runoffsource === "curvenumber"){
        requestJson.geometry["geometryMetadata"] = {
            "precipSource": precip
        }
    }
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
            taskID = data.job_id;
            jobID = data.job_id;
            var model = $("#model_name").html();
            var submodule = $("#submodule_name").html();
            setDataRequestCookie(taskID);
            window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
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
    // counter = counter - 1;
    var url = $("#page_url").html();
    var requestUrl = url + "/hms/rest/api/v2/hms/data";
    if (counter > 0) {
        $.ajax({
            type: "GET",
            url: requestUrl + "?job_id=" + taskID,
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
                    setOutputUI();
                    toggleLoader(true, "");
                    setTitle();
                }
                else if (data.status === "FAILURE") {
                    toggleLoader(false, "Task " + taskID + " encountered an error.");
                    console.log("Task failed to complete.");
                    deleteTaskFromCookie(taskID);
                }
                else {
                    setTimeout(getDataPolling, 10000);
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
    }
    else {
        console.log("Failed to get data, reached polling cap.")
    }
    return false;
}

function getPreviousData() {
    taskID = $('#previous_task_id').val();
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
    return false;
}

function getPreviousDataFromID(id){
    taskID = id;
    var model = $("#model_name").html();
    var submodule = $("#submodule_name").html();
    window.location.href = "/hms/" + model + "/" + submodule + "/output_data/" + taskID + "/";
    return false;
}

// Leaflet map variables //
var layerESRI = L.esri.basemapLayer('Imagery');
var layerLabels;
var currentSelectedGeometry = null;
var mapSelectionInfo = L.control();
var addPopup = null;


function get_nhd_layer_queries(bbox){
    let base_url = nhd_plus_layers["url"];
    let huc_layers = nhd_plus_layers["layers"];
    let layer_queries = {};
    for(let [key, value] of Object.entries(huc_layers)){
        let q = "dynamicLayers=" + encodeURIComponent(JSON.stringify(value["dynamicLayers"])) +
            "&dpi=" + value["dpi"] +
            "&transparent=" + value["transparent"] +
            "&format=" + value["format"] +
            "&layers=" + value["layers"] +
            "&bbox=" + bbox["_southWest"]["lng"] + + "," + bbox["_southWest"]["lat"] + "," + bbox["_northEast"]["lng"] + "," + bbox["_northEast"]["lat"]  +
            "&bboxSR=900913" +
            "&imageSR=" + value["imageSR"] +          //900913
            "&size=" + value["size"] +
            "&_ts=" + value["_ts"] +
            "&f=" + value["f"];
        layer_queries[key] = base_url + q;
    }
    return layer_queries;
}


// Leaflet map functions //
function openHucMap() {
    $('#huc_map_block').fadeIn("faster");
    if (hucMap === null) {
        hucMap = L.map('huc_map_div', {renderer: L.svg({padding: 100})}).setView([40.265306, -98.623725], 4);
        L.esri.basemapLayer('Topographic').addTo(hucMap);
        for (var huc in huc_basemaps) {
            if (huc_basemaps.hasOwnProperty(huc)) {
                huc_basemaps[huc].setOpacity(0.4);
                huc_basemaps[huc].setZIndex(10);
                hucMap.addLayer(huc_basemaps[huc]);
            }
        }
        // let bbox = hucMap.getBounds();
        // let images_urls = get_nhd_layer_queries(bbox);
        // for(let [key, value] of Object.entries(images_urls)){
        //     L.imageOverlay(value, bbox).addTo(hucMap);
        // }
        hucMap.on("click", function (e) {
            // Check if click originated from mapSelectionInfo window
            if (window.navigator.userAgent.indexOf("Chrome") > -1) {
                if (e.originalEvent.path[0].id === "huc_map_div" || e.originalEvent.path[0].localName === "path") {
                    clickGetStreamComid(e);
                }
            }
            else if (window.navigator.userAgent.indexOf("Firefox") > -1) {
                if (e.originalEvent.originalTarget.attributes[0].nodeValue === "huc_map_div") {
                    clickGetStreamComid(e);
                }
            }
            else if (window.navigator.userAgent.indexOf("Edge") > -1) {
                clickGetStreamComid(e);
            }
            else {
                clickGetStreamComid(e);
            }
        });
        hucMap.on("zoomend", function () {
            var currentLevel = getHucFromZoom();
            var hucNum = currentLevel.slice(4, currentLevel.length);
            $('#current_huc_level').html(" - Currently viewing HUC " + hucNum + " boundaries")
        });
        mapSelectionInfo.onAdd = function () {
            this._div = L.DomUtil.create('div', 'selection_info');
            this.update();
            return this._div;
        };
        mapSelectionInfo.update = function () {
            var selectionInfo;
            if ($('#spatial_type').val() === "hucid") {
                selectionInfo = '<h4>HUC Selection Options</h4>' +
                    '<div id="selection_huc_options">' +
                    '<label class="selection_huc_button">HUC 8<input disabled type="radio" checked value="HUC_8" name="selected_huc_type"></label>' +
                    '<label class="selection_huc_button">HUC 12<input checked type="radio" value="HUC_12" name="selected_huc_type"></label>' +
                    '</div>' +
                    '<h4>HUC Selection Info</h4>' +
                    '<div id="selection_info_div">' +
                    '<div id="selection_id_div">ID: <span id="selection_id"></span></div>' +
                    '<div id="selection_name_div">Name: <span id="selection_name"></span></div>' +
                    '<div id="selection_area_div">Area: <span id="selection_area"></span>km<sup>2</sup></div>' +
                    '<div id="selection_state_div">State(s): <span id="selection_state"></span></div>' +
                    '</div>'
            }
            else {
                selectionInfo = '<h4>Catchment Selection Info</h4>' +
                    '<div id="selection_info_div">' +
                    '<div id="selection_id_div">ID: <span id="selection_id"></span></div>' +
                    '<div id="selection_huc12_div">HUC 12: <span id="selection_huc12"></span></div>' +
                    '<div id="selection_area_div">Area: <span id="selection_area"></span>km<sup>2</sup></div>' +
                    '<div id="selection_region_div">Region: <span id="selection_region"></span></div>' +
                    '</div>'
            }
            this._div.innerHTML = selectionInfo;
        };
        mapSelectionInfo.addTo(hucMap);
    }
    else{
        mapSelectionInfo.update = function () {
            var selectionInfo;
            if ($('#spatial_type').val() === "hucid") {
                selectionInfo = '<h4>HUC Selection Options</h4>' +
                    '<div id="selection_huc_options">' +
                    '<label class="selection_huc_button">HUC 8<input disabled type="radio" checked value="HUC_8" name="selected_huc_type"></label>' +
                    '<label class="selection_huc_button">HUC 12<input checked type="radio" value="HUC_12" name="selected_huc_type"></label>' +
                    '</div>' +
                    '<h4>HUC Selection Info</h4>' +
                    '<div id="selection_info_div">' +
                    '<div id="selection_id_div">ID: <span id="selection_id"></span></div>' +
                    '<div id="selection_name_div">Name: <span id="selection_name"></span></div>' +
                    '<div id="selection_area_div">Area: <span id="selection_area"></span>km<sup>2</sup></div>' +
                    '<div id="selection_state_div">State(s): <span id="selection_state"></span></div>' +
                    '</div>'
            }
            else {
                selectionInfo = '<h4>Catchment Selection Info</h4>' +
                    '<div id="selection_info_div">' +
                    '<div id="selection_id_div">ID: <span id="selection_id"></span></div>' +
                    '<div id="selection_huc12_div">HUC 12: <span id="selection_huc12"></span></div>' +
                    '<div id="selection_area_div">Area: <span id="selection_area"></span>km<sup>2</sup></div>' +
                    '<div id="selection_region_div">Region: <span id="selection_region"></span></div>' +
                    '</div>'
            }
            this._div.innerHTML = selectionInfo;
        };
        mapSelectionInfo.addTo(hucMap);
    }
    let currentHucInput = $('#huc_id').val();
    let currentComIDInput = $('#comid').val();
    if (currentHucInput !== undefined && currentHucInput.length === 12) {
        getHucDataById(currentHucInput);
    }
    else if (currentComIDInput !== undefined) {
        getStreamDataByComID(currentComIDInput);
    }

    return false;
}

function toggleHucMap() {
    $('#huc_map_block').fadeOut("faster");
    hucMap.closePopup();
    return false;
}

function setBasemap(basemap) {
    if (layerESRI) {
        hucMap.removeLayer(layerESRI);
    }
    layerESRI = L.esri.basemapLayer(basemap);
    hucMap.addLayer(layerESRI);
    if (layerLabels) {
        hucMap.removeLayer(layerLabels);
    }
    if (basemap === 'ShadedRelief' || basemap === 'Imagery' || basemap === 'Terrain') {
        layerLabels = L.esri.basemapLayer(basemap + 'Labels');
        hucMap.addLayer(layerLabels);
    }
}

function changeBasemap(basemaps) {
    var basemap = basemaps.value;
    setBasemap(basemap);
}

function clickGetStreamComid(e) {
    var coord = e.latlng;
    var lat = coord.lat;
    var lng = coord.lng;

    if ($('#spatial_type').val() === "hucid") {
        var hucType = $('#selection_huc_options input:checked').val();
        getHucData(hucType, lat, lng);
    }
    else {
        getStreamData(lat, lng);
    }
}

function getStreamData(lat, lng) {
    // COMID Request

    var url = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/Catchments_NP21_Simplified/MapServer/0/query?where=&text=&objectIds=&time=&geometry=%7B%22x%22+%3A+"
        + lng + "%2C+%22y%22+%3A+" + lat + "%2C+%22spatialReference%22+%3A+%7B%22wkid%22+%3A+4326%7D%7D&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelWithin&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=%7B%22wkt%22+%3A+%22GEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2C+SPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0%5D%2C+UNIT%5B%5C%22Degree%5C%22%2C0.017453292519943295%5D%5D%22%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    $.ajax({
        type: "GET",
        url: url,
        jsonp: true,
        async: false,
        success: function (data, status, jqXHR) {
            addCatchmentToMap(data);
        },
        error: function (jqXHR, status) {
            console.log("Error retrieving stream catchment data.");
        }
    });
    return false;
}

function getStreamDataByComID(comid) {
    // COMID Request
    var catchment_base_url = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/Catchments_NP21_Simplified/MapServer/0/query?where=FEATUREID=" + comid;
    var catchment_url_options = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=%7B%22wkt%22+%3A+%22GEOGCS%5B%5C%22GCS_WGS_1984%5C%22%2CDATUM%5B%5C%22D_WGS_1984%5C%22%2C+SPHEROID%5B%5C%22WGS_1984%5C%22%2C6378137%2C298.257223563%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0%5D%2C+UNIT%5B%5C%22Degree%5C%22%2C0.017453292519943295%5D%5D%22%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    var url = catchment_base_url + catchment_url_options;
    $.ajax({
        type: "GET",
        url: url,
        jsonp: true,
        async: false,
        success: function (data, status, jqXHR) {
            addCatchmentToMap(data);
        },
        error: function (jqXHR, status) {
            console.log("Error retrieving stream catchment data.");
        }
    });
    return false;
}

function getHucFromZoom() {
    let zoomLevel = hucMap.getZoom();
    if (zoomLevel < 5) {
        return "HUC_2";
    }
    else if (zoomLevel === 5) {
        return "HUC_4";
    }
    else if (zoomLevel === 6) {
        return "HUC_6";
    }
    else if (zoomLevel === 7 || zoomLevel === 8) {
        return "HUC_8";
    }
    else if (zoomLevel === 9) {
        return "HUC_10";
    }
    else if (zoomLevel > 9) {
        return "HUC_12";
    }
    else {
        return "HUC_12";
    }
}

function getHucData(hucType, lat, lng) {
    var baseUrl = "";
    var point = "&geometry={\"x\":" + lng + ",\"y\":" + lat + ",\"spatialReference\":{\"wkid\":4326}}";
    var outFields = "";
    var params = "&geometryType=esriGeometryPoint&inSR=&spatialRel=esriSpatialRelIntersects&returnGeometry=true&returnTrueCurves=false&geometryPrecision=&outSR=%7B%22wkid%22+%3A+4326%7D&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";

    if (hucType === "HUC_12") {
        baseUrl = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/0/query?where=&text=&time=";
        outFields = "&outFields=OBJECTID%2C+Shape%2C+GAZ_ID%2C+AREA_ACRES%2C+AREA_SQKM%2C+STATES%2C+LOADDATE%2C+HUC_2%2C+HU_2_NAME%2C+HUC_4%2C+HU_4_NAME%2C+HUC_6%2C+HU_6_NAME%2C+HUC_8%2C+HU_8_NAME%2C+HUC_10%2C+HU_10_NAME%2C+HUC_12%2C+HU_12_NAME%2C+HU_12_TYPE%2C+HU_12_MOD%2C+NCONTRB_ACRES%2C+NCONTRB_SQKM%2C+HU_10_TYPE%2C+HU_10_MOD%2C+Shape_Length%2C+Shape_Area";
    }
        // else if (hucType === "HUC_10"){
        //     baseUrl = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/1/query?where=&text=&time=";
        //     outFields = "&outFields=OBJECTID%2C+Shape%2C+GAZ_ID%2C+AREA_ACRES%2C+AREA_SQKM%2C+STATES%2C+LOADDATE%2C+HUC_2%2C+HU_2_NAME%2C+HUC_4%2C+HU_4_NAME%2C+HUC_6%2C+HU_6_NAME%2C+HUC_8%2C+HU_8_NAME%2C+HUC_10%2C+HU_10_NAME%2C+NCONTRB_ACRES%2C+NCONTRB_SQKM%2C+HU_10_TYPE%2C+HU_10_MOD%2C+Shape_Length%2C+Shape_Area";
    // }
    else {
        hucType = "HUC_8";
        baseUrl = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/2/query?where=&text=&time=";
        outFields = "&outFields=OBJECTID%2C+Shape%2C+GAZ_ID%2C+AREA_ACRES%2C+AREA_SQKM%2C+STATES%2C+LOADDATE%2C+HUC_2%2C+HU_2_NAME%2C+HUC_4%2C+HU_4_NAME%2C+HUC_6%2C+HU_6_NAME%2C+HUC_8%2C+HU_8_NAME%2C+Shape_Length%2C+Shape_Area";
    }
    var queryString = point + outFields + params;
    getEPAWatersData(baseUrl, queryString, hucType)
}

function getHucDataById(hucID) {
    var baseUrl = "";
    var whereCondition = "";
    var outFields = "";
    var params = "&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson";
    var queryString = "";
    if (hucID.length === 8) {
        baseUrl = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/2/query?";
        whereCondition = "where=HUC_8+LIKE+%28%27" + hucID + "%27%29";
        outFields = "&outFields=OBJECTID%2C+Shape%2C+GAZ_ID%2C+AREA_ACRES%2C+AREA_SQKM%2C+STATES%2C+LOADDATE%2C+HUC_2%2C+HU_2_NAME%2C+HUC_4%2C+HU_4_NAME%2C+HUC_6%2C+HU_6_NAME%2C+HUC_8%2C+HU_8_NAME%2C+Shape_Length%2C+Shape_Area";
        queryString = whereCondition + outFields + params;
        getEPAWatersData(baseUrl, queryString, "HUC_8");
    }
    else if (hucID.length === 12) {
        baseUrl = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/0/query?";
        whereCondition = "where=HUC_12+LIKE+%28%27" + hucID + "%27%29";
        outFields = "&outFields=OBJECTID%2C+Shape%2C+GAZ_ID%2C+AREA_ACRES%2C+AREA_SQKM%2C+STATES%2C+LOADDATE%2C+HUC_2%2C+HU_2_NAME%2C+HUC_4%2C+HU_4_NAME%2C+HUC_6%2C+HU_6_NAME%2C+HUC_8%2C+HU_8_NAME%2C+HUC_10%2C+HU_10_NAME%2C+HUC_12%2C+HU_12_NAME%2C+HU_12_TYPE%2C+HU_12_MOD%2C+NCONTRB_ACRES%2C+NCONTRB_SQKM%2C+HU_10_TYPE%2C+HU_10_MOD%2C+Shape_Length%2C+Shape_Area";
        queryString = whereCondition + outFields + params;
        getEPAWatersData(baseUrl, queryString, "HUC_12");
    }
}

function addCatchmentToMap(data) {
    if (currentSelectedGeometry !== null) {
        hucMap.removeLayer(currentSelectedGeometry);
    }
    var hucData = data;
    if (typeof data === "string") {
        hucData = JSON.parse(data);
    }
    currentSelectedGeometry = L.geoJSON(hucData);
    currentSelectedGeometry.addTo(hucMap);
    hucMap.fitBounds(currentSelectedGeometry.getBounds());
    var comid = hucData.features[0].properties.FEATUREID;
    $('#comid').val(comid);
    $('#selection_id').html(comid);
    $('#selection_huc12').html(hucData.features[0].properties.WBD_HUC12);
    $('#selection_area').html(Number(hucData.features[0].properties.AREASQKM).toFixed(4));
    $('#selection_region').html(hucData.features[0].properties.NHDPLUS_REGION);
    $('#add_spatial_input').removeClass("blocked");
    setTimeout(function () {
        if (addPopup !== null) {
            hucMap.removeLayer(addPopup);
        }
        addPopup = L.popup({
            keepInView: true,
        }).setLatLng(hucMap.getCenter())
            .setContent('<button id="huc_map_button_add" type="button" onclick="addSpatialInput(); toggleHucMap(); return false;">Add Catchment: ' + comid + '</button>')
            .openOn(hucMap);
    }, 600);
}

function addHucToMap(data, hucType) {
    if (currentSelectedGeometry !== null) {
        hucMap.removeLayer(currentSelectedGeometry);
    }
    var hucData = data;
    if (typeof data === "string") {
        hucData = JSON.parse(data);
    }
    var hucNum = hucType.slice(4, hucType.length);
    var hucID = hucData.features[0].properties[hucType];
    currentSelectedGeometry = L.geoJSON(hucData);
    currentSelectedGeometry.addTo(hucMap);
    $('#selection_id').html(hucID);
    $('#selection_name').html(hucData.features[0].properties["HU_" + hucNum + "_NAME"]);
    $('#selection_area').html(Number(hucData.features[0].properties.AREA_SQKM).toFixed(4));
    $('#selection_state').html(hucData.features[0].properties.STATES);
    hucMap.fitBounds(currentSelectedGeometry.getBounds());
    $('#huc_id').val(hucID);
    $('#add_spatial_input').removeClass("blocked");
    setTimeout(function () {
        if (addPopup !== null) {
            hucMap.removeLayer(addPopup);
        }
        addPopup = L.popup({
            keepInView: true,
        }).setLatLng(hucMap.getCenter())
            .setContent('<button id="huc_map_button_add" type="button" onclick="addSpatialInput(); toggleHucMap(); return false;">Add HUC: ' + hucID + '</button>')
            .openOn(hucMap);
    }, 600);
}

function getEPAWatersData(url, params, hucType) {
    $.ajax({
        type: "GET",
        url: url + params,
        jsonp: true,
        async: false,
        success: function (data, status, jqXHR) {
            addHucToMap(data, hucType);
        },
        error: function (jqXHR, status) {
            console.log("Error retrieving stream segment data.");
        }
    });
}
//
// function loadCookies(){
//     var url = window.location.href.split('/');
//     var model = $("#model_name").html();
//     var submodule = $("#submodule_name").html();
//     url = url[2] + "/hms/" + model + "/" + submodule;
//     var cookie = getCookie(url);
//     cookie = pruneCookieTasks(cookie);
//     var ids = cookie.split(",");
//     if( ids.length > 1){
//         $("#previous_tasks").show();
//         var list = $('#previous_tasks_list')[0];
//         ids.forEach(function(id){
//             if(id !== "") {
//                 var id_time = id.split(':');
//
//                 var eleID = document.createElement("span");
//                 eleID.innerText = id_time[0];
//                 eleID.className = "previous_task_id";
//                 eleID.setAttribute("title", "Task ID");
//                 eleID.onclick = function () {
//                     getPreviousDataFromID(id_time[0]);
//                 };
//
//                 var eleT = document.createElement("span");
//                 var d = new Date(parseInt(id_time[1]));
//                 eleT.innerText = d.toLocaleString();
//                 eleT.className = "previous_task_time";
//                 eleT.setAttribute("title", "Task Timestamp");
//
//                 var ele = document.createElement("li");
//                 ele.className = "previous_task";
//                 ele.appendChild(eleID);
//                 ele.appendChild(eleT);
//                 list.appendChild(ele);
//             }
//         });
//     }
// }
//
// function setDataRequestCookie(taskID){
//     var daysToExpire = 1;
//     var date = new Date();
//     date.setTime(date.getTime() + daysToExpire * 24*60*60*1000);
//     var expires = "expires=" + date.toUTCString();
//     var timestamp = new Date();
//     var taskIDs = taskID + ":" + timestamp.getTime();
//     var url = window.location.href.split('/');
//     var model = $("#model_name").html();
//     var submodule = $("#submodule_name").html();
//     url = url[2] + "/hms/" + model + "/" + submodule;
//     var current = getCookie(url);
//     current = pruneCookieTasks(current);
//     var ids = "";
//     $.each(current.split(','), function(index, value){
//         var id = value.split(':')[0];
//         if(id !== taskID && id !== ""){
//             ids += "," + value;
//         }
//         else if(id === taskID){
//             taskIDs = value;
//         }
//     });
//
//     taskIDs = taskIDs + ids;
//     document.cookie = url+  "=" + taskIDs + ";" + expires + ";path=" + "/hms/" + model + "/" + submodule + "/";
// }
//
// function getCookie(cname) {
//     var name = cname + "=";
//     var decodedCookie = decodeURIComponent(document.cookie);
//     var ca = decodedCookie.split(';');
//     for(var i = 0; i <ca.length; i++) {
//         var c = ca[i];
//         while (c.charAt(0) == ' ') {
//             c = c.substring(1);
//         }
//         if (c.indexOf(name) == 0) {
//             return c.substring(name.length, c.length);
//         }
//     }
//     return "";
// }
//
// function pruneCookieTasks(currentTasks){
//     var IDs = currentTasks.split(',');
//     var taskIDs = "";
//     var now = new Date();
//     now.setDate(now.getDate() - 1);
//     now = now.getTime();
//     $.each(IDs, function(k, v){
//         if(v !== "") {
//             var timestamp = new Date();
//             if (v.includes(":")) {
//                 var id_t = v.split(':');
//                 timestamp.setTime(parseInt(id_t[1]));
//                 if (timestamp.getTime() > now) {
//                     taskIDs = taskIDs + "," + v;
//                 }
//             } else {
//                 taskIDs = taskIDs + "," + v + ":" + timestamp.getTime();
//             }
//         }
//     });
//     return taskIDs;
// }
//
// function deleteTaskFromCookie(id){
//     var url = window.location.href.split('/');
//     var model = $("#model_name").html();
//     var submodule = $("#submodule_name").html();
//     url = url[2] + "/hms/" + model + "/" + submodule;
//     var current = getCookie(url);
//     current = pruneCookieTasks(current);
//     var IDs = current.split(',');
//     var validIDs = [];
//     $.each(IDs, function(k, v){
//         if(v.includes(":")){
//             var i = v.split(':');
//             if(i[0] !== id){
//                 validIDs.push(v);
//             }
//         }
//     });
//     var daysToExpire = 1;
//     var date = new Date();
//     date.setTime(date.getTime() + daysToExpire * 24*60*60*1000);
//     var expires = "expires=" + date.toUTCString();
//     var taskIDs = validIDs.join();
//     document.cookie = url+  "=" + taskIDs + ";" + expires + ";path=" + "/hms/" + model + "/" + submodule + "/";
// }
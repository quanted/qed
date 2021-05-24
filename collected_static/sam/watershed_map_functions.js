
//  create placeholder global variables
var comid = null;
var selectedHuc = null;
var selectedHuc12;
// sets variable for selected stream
var selectedStream;
var selectedIntake;
var selectedHucName = null;
var selectedHucNumber = null;
var selectedHucArea = null;
var summaryHUC8Data;
var summaryHUC12Data;
var outputData;
var mode; // no longer needed?
var hucsRun = [];
var huc8ColorLayer;
var legend;
var region = '07';
var huc12_json;

// specify field (placeholder)
var field = "chronic_em_inv";

//print to console for debuggin?
var DEBUG = false;


$(document).ready(function () {
    $('#csvSave').on("click", saveTableAsCSV);
});

//helper function that works across all browsers
function contains(a, obj) {
    for (var i = 0; i < a.length; i++) {
        if (a[i] === obj) {
            return true;
        }
    }
    return false;
}

// handler for a stream click
function onStreamMapClick(e) {
    if(selectedHuc != null){
        map.removeLayer(selectedHuc);
    }
    getStreamData(e.latlng.lat, e.latlng.lng);
    map.closePopup();
}


// set to hide huc coloring when zoomed to stream level
function setZoomHandler(){
    map.on('zoomend', function() {
        if (map.getZoom() >=11){
            if (map.hasLayer(huc8ColorLayer)) {
                map.removeLayer(huc8ColorLayer);
                //map.removeControl(legend);
            }
            if(! map.hasLayer(huc12s)){
                map.addLayer(huc12s);
            }
            huc12s.setStyle({interactive:false});
        }
        if (map.getZoom() < 11){ //huc12 geojson layer is currently overrulling this click level
            if(! map.hasLayer(huc12s)){
                map.addLayer(huc12s);
            }
            if (map.hasLayer(huc8ColorLayer)) {
                map.removeLayer(huc8ColorLayer);
            }
            huc12s.setStyle({interactive:true});

        }
        if (map.getZoom() < 9){
            if(map.hasLayer(huc12s)){
                map.removeLayer(huc12s);
                huc12s.setStyle({interactive:true});
            }
            if (! map.hasLayer(huc8ColorLayer)){
                map.addLayer(huc8ColorLayer);
                //map.addControl(legend);
            }
        }
        map.invalidateSize(); //test first


    });
}


//ajax call using lat long for stream data and shapefile
function getStreamData(lat, lng) {
    var url = "https://ofmpub.epa.gov/waters10/PointIndexing.Service";
    var latitude = lat.toString();
    var longitude = lng.toString();
    $('#latVal').html(Number(latitude).toFixed(6));
    $('#lngVal').html(Number(longitude).toFixed(6));

    var ptIndexParams = {
        'pGeometry': 'POINT(' + longitude + ' ' + latitude + ')'
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
        success: function (data, status, jqXHR) {
            var streamData = JSON.parse(data);
            var selectedComid = streamData.output.ary_flowlines[0].comid;
            var wantedData = outputData.features.filter(function (i) {
                return (i.properties.COMID == selectedComid);
            });
            $('#boxid').html(selectedComid);
            addStreamSeg(streamData, selectedComid);
            if(wantedData.length == 0){
                $('#pestTable').hide();
                $('#saveTable').hide();
                DEBUG && console.log("Selected stream was not included in SAM run");
                return false;
            }
            setTimeout(populateFilteredTable(wantedData[0].properties), 300);
            return false;
        },
        error: function (jqXHR, status) {
            $('#boxid').html("Error attempting to get river data.");
            return false;
        }
    });
}


<!--- add stream to map -->
function addStreamSeg(streamData, comid) {
    DEBUG && console.log(comid);
    var latlon = streamData.output.ary_flowlines[0].shape.coordinates.map(function (c) {
        return c.reverse();
    });
    if (map.hasLayer(selectedStream)) {
        map.removeLayer(selectedStream);
    }
    selectedStream = L.polyline(latlon, {
        color: '#02bfe7',
        weight: 8,
        opacity: 0.9,
        lineJoin: 'round'
    }).addTo(map);
    map.fitBounds(selectedStream.getBounds());
}


// populate exceedance table for the selected stream (below map)
function populateFilteredTable(data) {
    //convert object into an array of objects
    var dataHtml = "<h4 style=\"text-align: center; width: 100%\">Probability of Pesticide Concentration Exceedance</h4>" +
        "<table id='samWatershedTable'>" +
        "<thead style='display:none;'><th></th><th></th><th></th><th></th><th></th><th></th></thead>" +
        "<tbody>" +
        "<tr><td id='tbl_col'>Acute Em Fish</td><td>" + Number(data["acute_em_fish"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Em Fish</td><td>" + Number(data["chronic_em_fish"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Em Fish</td><td>" + Number(data["overall_em_fish"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Em Inv</td><td>" + Number(data["acute_em_inv"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Em Inv</td><td>" + Number(data["chronic_em_inv"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Em Inv</td><td>" + Number(data["overall_em_inv"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Fw Fish</td><td>" + Number(data["acute_fw_fish"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Fw Fish</td><td>" + Number(data["chronic_fw_fish"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Fw Fish</td><td>" + Number(data["overall_fw_fish"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Fw Inv</td><td>" + Number(data["acute_fw_inv"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Fw Inv</td><td>" + Number(data["chronic_fw_inv"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Fw Inv</td><td>" + Number(data["overall_fw_inv"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Human</td><td>" + Number(data["acute_human"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Human</td><td>" + Number(data["chronic_human"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Human</td><td>" + Number(data["overall_human"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Nonvasc Plant</td><td>" + Number(data["acute_nonvasc_plant"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Nonvasc Plant</td><td>" + Number(data["chronic_nonvasc_plant"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Nonvasc Plant</td><td>" + Number(data["overall_nonvasc_plant"]).toFixed(3) + "</td></tr>" +
        "<tr><td id='tbl_col'>Acute Vasc Plant</td><td>" + Number(data["acute_vasc_plant"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Chronic Vasc Plant</td><td>" + Number(data["chronic_vasc_plant"]).toFixed(3) + "</td>" +
        "<td id='tbl_col'>Overall Vasc Plant</td><td>" + Number(data["overall_vasc_plant"]).toFixed(3) + "</td></tr>" +
        "</tbody>" +
        "</table>";
    $('#pestTable').html(dataHtml);
    $('#pestTable').show();
    $('#saveTable').show();
}


function saveTableAsCSV() {
    var data = "";
    var config = {
        sorting: false,
        searching: false,
        paging: false,
        bInfo: false
    };
    var dt = $('#samWatershedTable').dataTable(config);
    dt.rows().data().map(function (r) {
        data += r.toString() + "\n";
    });
    var mainHeader = "SAM Pesticide Probabilities \n";
    var metaHeader = "COMID, Latitude, Longitude \n";
    var metadata = $('#boxid').html() + ", " + $('#latVal').html() + ", " + $('#lngVal').html() + "\n";
    var fileName = "SAM_pesticide_" + comid;
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:data:text/csv;charset=utf-8,' + encodeURIComponent(mainHeader + "\n" + metaHeader + metadata + "\n" + data));
    pom.setAttribute('download', fileName + '.csv');
    if (document.createEvent) {
        var event = document.createEvent('MouseEvents');
        event.initEvent('click', true, true);
        pom.dispatchEvent(event);
    }
    else {
        pom.click();
    }
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



// creates a huc8 layer on top of the other huc8 layer that contains only the huc8s that were run.
// we can interact with this layer without doing anything to the huc8s that weren't run, saving us
// computation time on the client-side
function hucColorLayer(){
    huc8ColorLayer = L.geoJson(huc8s, {
    style: hucStyle,
    filter: function(feature) {
        huc_8 = feature.properties.HUC_CODE;
        if (contains(hucsRun, huc_8)) {
            return true;
        }
        else {
            return false;
        }
    }
    }).addTo(map);

}



// function to read SAM stream level output
function readOutputJSON() {
    var key = getCookie('task_id');
    // TODO: change to correct base url
    var url = "/pram/rest/pram/sam/data/" + key.toString();
    var samOutput = null;
    $.ajax({
        type: "GET",
        url: url,
        async: true,
        success: function (data) {
            DEBUG && console.log("Read output JSON from file: " + url.toString());
            DEBUG && console.log("Output JSON data contents...");
            DEBUG && console.log(data.toString());
            samOutput = data;
            outputData = data;
            return false;
        },
        error: function (jqXHR, status) {
            DEBUG && console.log("Failed to retrieve output json data.");
            $('#boxid').html("Error attempting to get river data.");
            return false;
        }
    });
    return samOutput
}


//function to read the SAM postprocessing summary stats through the django-to-flask proxy (HUC8s)
function readSummaryHUC8JSON() {
    var key = getCookie('task_id');
    // TODO: change to correct base url
    var url = "/pram/rest/pram/sam/summary/huc8/" + key.toString();
    var samOutput = null;
    $.ajax({
        type: "GET",
        url: url,
        async: true,
        success: function (data) {
            DEBUG && console.log("Read summary JSON from file: " + url.toString());
            //DEBUG && console.log("Output JSON data contents...");
            //DEBUG && console.log(data.toString());
            samOutput = data;
            summaryHUC8Data = data;
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    hucsRun.push(key);  //track which hucs were actually run!
                }
            }
            readSummaryHUC12JSON(); //async ajax call
            hucColorLayer(); //create a layer for the shaded hucs
            addHUC8Statistics(); //add the huc8 stats to the huc8 layer
            colorHUC8s($('#fieldselect').val(), $('#summaryselect').val()); //color the hucs
            addStreams(); //add the stream layer
            addIntakes(); //add the drinking water intake marker layergroup
            addHucLegend();
            map.invalidateSize();
            //addColoredStreams(region);
            //setZoomHandler();
            return false;
        },
        error: function (jqXHR, status) {
            DEBUG && console.log("Failed to retrieve output json data.");
            $('#boxid').html("Error attempting to get watershed data.");
            return false;
        }
    });
    return samOutput
}

//function to read the SAM postprocessing summary stats through the django-to-flask proxy (HUC12s)
function readSummaryHUC12JSON() {
    var key = getCookie('task_id');
    // TODO: change to correct base url
    var url = "/pram/rest/pram/sam/summary/huc12/" + key.toString();
    var samOutput = null;
    $.ajax({
        type: "GET",
        url: url,
        async: true,
        success: function (data) {
            DEBUG && console.log("Read summary JSON from file: " + url.toString());
            //DEBUG && console.log("Output JSON data contents...");
            //DEBUG && console.log(data.toString());
            samOutput = data;
            summaryHUC12Data = data;
            addHUC12s(); //ajax async call
            return false;
        },
        error: function (jqXHR, status) {
            DEBUG && console.log("Failed to retrieve output json data.");
            $('#boxid').html("Error attempting to get watershed data.");
            return false;
        }
    });
    return samOutput
}



// sets the HUC color based on a summary stat
function exceedanceColor(d) {
    if (d == null) {
        return '#93D4BC'
    } else if (d > 0.5) {
        return "#d73027"
    } else if (d > 0.4) {
        return "#fc8d59"
    } else if (d > 0.3) {
        return "#fee090"
    } else if (d > 0.2) {
        return "#F8D0C7"
    } else if (d > 0.1) {
        return "#d0b3db"
    } else {
        return "#4575b4"
    }
}

// sets HUC fill opacity to be higher if there is data on the HUC
function getHUCFillOpacity(d) {
    if (d == null) {
        return 0.2;
    } else {
        return 0.4;
    }
}


//stream style
function streamStyle(feature, field) {
    return {
        weight: 1,
        opacity: 1,
        color: exceedanceColor(feature.properties[field])
    };
}


//huc8 initial style
function hucStyle(feature) {
    return {
        fillColor: getColor(),
        weight: .3,
        opacity: 0.9,
        color: 'black',
        fillOpacity: 0.0 // clear
    };
}


//style HUC polygon - default
function getColor() {
    return '#93D4BC'
}


//style the downloaded selected huc8 shapefile - setting to invisible because it is not simplified like the base layer
var hucStyleSelected = {
    fillColor: 'white',
    weight: 0.0,
    opacity: 0.0,
    color: 'black',
    fillOpacity: 0.0
};


//style HUC8's based on summary statistics of a given toxicity threshold exceedance probability
function colorHUC8s(fieldVal, summary_stat) {
    huc8ColorLayer.setStyle(function(feature) {
        stat = feature.properties.summary[fieldVal + "_" + summary_stat];
        return {
            fillColor: exceedanceColor(stat),
            weight: .3,
            opacity: 0.9,
            color: 'black',
            fillOpacity: getHUCFillOpacity(stat),
            minZoom: 0,
            maxZoom: 10
        }
    });
    //map.setView(start_point, start_zoom); //with canvas rendering doing a map pan/zoom seems needed to see the layers
}


//style HUC12's based on summary statistics of a given toxicity threshold exceedance probability
function colorHUC12s(fieldVal, summary_stat) {
    huc12s.setStyle(function(feature) {
        stat = feature.properties.summary[fieldVal + "_" + summary_stat];
        return {
            fillColor: exceedanceColor(stat),
            weight: .3,
            opacity: 0.9,
            color: 'black',
            fillOpacity: getHUCFillOpacity(stat),
            minZoom: 0,
            maxZoom: 10
        }
    });
}


// for the selected HUC8 (clicked), set border to be thicker
function setSelectedHUC8(hucID) {
    huc8Layer.setStyle({weight: 0.3});
    huc8Layer.setStyle(function(feature) {
        if(feature.properties.HUC_CODE == hucID){
            return {
                weight: 2.0
            }
        }
    });
}


// called when huc12 layer is clicked, sets the clicked feature to be outlined
function setSelectedHUC12(layer){
    huc12s.setStyle({weight: 0.3});
    layer.setStyle({weight:2.0});
    selectedHuc12 = layer;
}



// returns the huc8 feature for a given huc8 ID
function fetchHUC8Shape(hucID){
    DEBUG && console.log(hucID);
    var out = huc8s.features.filter(function(x) { return x.properties.HUC_CODE == hucID})[0];
    return out;
}

//returns a given summary stat for a hucID, from the huc8 geojson
function fetchHUC8LayerData(hucID, summary_stat){
    feat = fetchHUC8Shape(hucID);
    return feat.properties.summary[summary_stat]
}


// returns the huc12 feature for a given huc12 ID
function fetchHUC12Shape(hucID){
    DEBUG && console.log(hucID);
    var out = huc12_json.features.filter(function(x) { return x.properties.HUC_12 == hucID})[0];
    return out;
}

//returns a given summary stat for a huc12, from the huc12 geojson
function fetchHUC12LayerData(hucID, summary_stat){
    feat = fetchHUC12Shape(hucID);
    return feat.properties.summary[summary_stat]
}


function clearMap() {
    map.eachLayer(function (layer) {
        map.removeLayer(layer);
    });
}


//grab huc8 summary stats for a certain huc, from the object created in watershed_map_scripts.js
function fetchHUC8Statistics(huc_code) {
    if(summaryHUC8Data[huc_code] != null) {
        return summaryHUC8Data[huc_code]
    }
    else {
        return 'not_run'
    }
}


//grab huc12 summary stats for a certain huc
function fetchHUC12Statistics(huc_code) {
    if(summaryHUC12Data[huc_code] != null) {
        return summaryHUC12Data[huc_code]
    }
    else {
        return 'not_run'
    }
}


// append huc8 summary statistics as properties in the huc8 geojson
function addHUC8Statistics() {
    for (var i = 0; i < huc8s.features.length; i++) {
        huc8s.features[i].properties.summary = fetchHUC8Statistics(huc8s.features[i].properties.HUC_CODE)
    }
}


// append huc12 summary statistics (from SAM) as properties in the huc12 geojson
function addHUC12Statistics() {
    for (var i = 0; i < huc12_json.features.length; i++) {
        huc12_json.features[i].properties.summary = fetchHUC12Statistics(huc12_json.features[i].properties.HUC_12)
    }
}


// Content for the popup bubble, based on the selected huc's id number and name and area
function popupContent(hucNumber, hucName, hucArea){
    var e1 = document.createElement('div');
    e1.classList.add("huc_popup");
    e1.innerHTML = '<h3> <strong> Watershed Summary </strong></h3>';
    e1.innerHTML += '<strong>HUC#: </strong>' + hucNumber + '<br><strong>' + 'Name: </strong>' + hucName;
    e1.innerHTML += '<br><strong> Catchment area: </strong>' + Number(hucArea).toFixed(2) + ' km'+'2'.sup();
    summary_select = $('#summaryselect').val();
    summary_stat = $('#fieldselect').val() + '_' + summary_select;
    e1.innerHTML += '<br><strong>' + summary_select.replace(new RegExp('^'+summary_select[0]+''), summary_select[0].toUpperCase()) +
        ' probability of exceedance: </strong><br>';
    if(hucNumber.length == 8){
            prob = Number(fetchHUC8LayerData(hucNumber, summary_stat)).toFixed(2);
    } else{
        prob = Number(fetchHUC12LayerData(hucNumber, summary_stat)).toFixed(2);
    }
    if(isNaN(prob)){prob = "Not calculated";}
    e1.innerHTML += prob;
    return e1;
}


//fetch a huc shapefile and info based on a click lon/lat
function GetHuc(latitude, longitude) {
    var hucLvl = 2; //HUC8
    var tempHuc = (12 - hucLvl * 2);
    var hucURL = "https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/" +
        hucLvl + "/query?geometry=%7B%22x%22+%3A+" + longitude + "%2C+%22y%22+%3A+" + latitude +
        "%2C+%22spatialReference%22+%3A+%7B%22wkid%22+%3A+4326%7D%7D&geometryType=esriGeometryPoint&" +
        "inSR=%7B%22wkid%22+%3A+4326%7D&spatialRel=esriSpatialRelWithin&outFields=HUC_" + tempHuc +
        "%2C+STATES%2C+Shape%2C+AREA_SQKM%2C+HU_" + tempHuc + "_NAME&" +
        "returnGeometry=true&returnTrueCurves=false&outSR=%7B%22wkid%22+%3A+4326%7D&returnIdsOnly=false&" +
        "returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=false&returnExtentsOnly=false&f=pjson";
    $.ajax({
        url: hucURL,
        method: 'GET',
        crossDomain: true,
        cache: true, //for now won't work b/c the api response forbids caching
        success: function (result_huc) {
            if (selectedHuc !== null) {
                map.removeLayer(selectedHuc);
            }
            // Convert HUC json data to valid geojson.
            var huc_data = JSON.parse(result_huc.replace("rings", "coordinates"));
            huc_data["type"] = "FeatureCollection";
            huc_data["features"][0]["type"] = "Feature";
            huc_data["features"][0]["properties"] = {};
            huc_data["features"][0]["geometry"]["type"] = "Polygon";
            selectedHuc = L.geoJSON(huc_data, {
                style: hucStyleSelected,
                onEachFeature: function onEachFeature(feature, layer) {
                    layer.on('click', function(e) {
                        var zoomLvl = map.getZoom();
                        if(zoomLvl >= 11) {
                            onMapClick(e);
                        }
                    });
                }
            }).addTo(map);
            selectedHucNumber = huc_data["features"][0]["attributes"]["HUC_" + tempHuc];
            selectedHucName = huc_data["features"][0]["attributes"]["HU_" + tempHuc + "_NAME"];
            selectedHucArea = huc_data["features"][0]["attributes"]["AREA_SQKM"];
            setSelectedHUC8(selectedHucNumber);
            //map.fitBounds(selectedHuc.getBounds());
            selectedHuc.bindPopup(popupContent(selectedHucNumber, selectedHucName, selectedHucArea)).openPopup();
            if(map.getZoom() > 8){
                map.setZoom(8,{animate:false});
            }
            map.panTo(selectedHuc.getBounds().getCenter(),{animate:false});
            //map.setContent('Selected');
        },
        error: function () {
            $('#hucNumber').html("ERROR: Unable to download data for selected HUC");
        }
    })
}


// HUC8 on click action
function hucOnClick(e){
    GetHuc(e.latlng.lat, e.latlng.lng);
}


// Overall click handler - if zoomed in to stream level, routes to stream map click handler,
//                         if zoomed to huc8 level, routes to huc8 click handler
//                         if zoomed to huc12 level, the code here should not run run as it will be intercepted by the
//                          huc12 layer's own onclick handler
function onMapClick(e){
    var zoomLvl = map.getZoom();
    if(zoomLvl >= 11) {
        map.closePopup();
        onStreamMapClick(e);
        return;
    } else if(zoomLvl >=9){
        if (map.hasLayer(selectedStream)) {
            map.removeLayer(selectedStream);
        }
        $('#pestTable').hide();
        $('#saveTable').hide();
        $('#latVal').html("");
        $('#lngVal').html("");
        $('#boxid').html("");
    } else{
        if (map.hasLayer(selectedStream)) {
            map.removeLayer(selectedStream);
        }
        $('#pestTable').hide();
        $('#saveTable').hide();
        $('#latVal').html("");
        $('#lngVal').html("");
        $('#boxid').html("");
        hucOnClick(e);
    }
}



// refresh the map, popup content, and info box to reflect new settings
function refreshOutput(newfield, summaryfield) {
    colorHUC8s(newfield.value, summaryfield.value);//$('#summaryselect').val());
    colorHUC12s(newfield.value, summaryfield.value);//$('#summaryselect').val());
    map.invalidateSize();
    if(selectedHuc != null){
        setSelectedHUC8(selectedHucNumber);
        selectedHuc.setPopupContent(popupContent(selectedHucNumber, selectedHucName));
    }
    huc12s.eachLayer(function(layer){
                layer._popup.setContent(popupContent(layer.feature.properties.HUC_12, layer.feature.properties.HU_12_NAME,
                        layer.feature.properties.AREA_SQKM));});
    if(selectedHuc12 != null){
        setSelectedHUC12(selectedHuc12); //redraw the bold lines if a huc12 was selected b/c colorHUC12 reset the lines
    }
}




var layerLabels;

function setBasemap(basemap) {
    if (layer) {
        map.removeLayer(layer);
    }

    layer = L.esri.basemapLayer(basemap);

    map.addLayer(layer);

    if (layerLabels) {
        map.removeLayer(layerLabels);
    }

    if (basemap === 'ShadedRelief'
        || basemap === 'Imagery'
        || basemap === 'Terrain'
        || basemap === 'Topographic'
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

//L.control.layers(streamNetwork).addTo(map);
function addStreams() {
    L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
        layers: 4,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }).addTo(map);
}

//------------ HUC12 shapes ------------//


//fetch the huc12s inside each huc8 that was actually run
function addHUC12s() {
    var huc8_string = hucsRun.join('%27%2C+%27');
    var url = 'https://watersgeo.epa.gov/arcgis/rest/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/0/query?where=' +
        'HUC_8+IN+%28%27' + huc8_string + '%27%29&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=' +
        '&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=HUC_12%2C+HU_12_NAME%2C+AREA_SQKM&returnGeometry=true&returnTrueCurves=' +
        'false&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&' +
        'groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=' +
        '&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson';
    $.ajax({
        url: url,
        method: 'GET',
        crossDomain: true,
        cache: true, //for now won't work b/c the api response forbids caching
        success: function (result_huc12s) {
            if (selectedHuc !== null) {
                map.removeLayer(selectedHuc);
            }
            huc12_json = JSON.parse(result_huc12s);
            delete huc12_json["crs"];
            huc12s = L.geoJSON(huc12_json, {
                style: hucStyle,
                onEachFeature: function onEachFeature(feature, layer) {
                    layer.on('click', function(e) {
                        var zoomLvl = map.getZoom();
                        if(zoomLvl >= 11) {   //currently redundant as this layer is set to non-interactive at zoom>=11
                            onMapClick(e);
                        } else{
                            setSelectedHUC12(layer);
                            if (map.hasLayer(selectedStream)) {
                                map.removeLayer(selectedStream);
                            }
                            $('#pestTable').hide();
                            $('#saveTable').hide();
                            $('#latVal').html("");
                            $('#lngVal').html("");
                            $('#boxid').html("");
                        }
                    });
                }
            });
            setZoomHandler();
            addHUC12Statistics(); //add the huc8 stats to the huc12 layer
            colorHUC12s($('#fieldselect').val(), $('#summaryselect').val()); //color the hucs
            huc12s.eachLayer(function(layer){
                layer.bindPopup(popupContent(layer.feature.properties.HUC_12, layer.feature.properties.HU_12_NAME,
                        layer.feature.properties.AREA_SQKM));
            });
            map.invalidateSize();
        },
        error: function () {
            console.log("ERROR: Unable to download data for HUC12s");
        }
    })
}




//------------ DRINKING WATER INTAKES ------------//

var intakes;
var intakeMarkers = new L.LayerGroup();

//function to set the popup content for an intake click
function intakeContent(feature){
    var in_comid = feature.properties.COMID;
    var in_sourceName = feature.properties.SourceName;
    var in_systemName = feature.properties.SystemName;
    var e1 = document.createElement('div');
    e1.classList.add("intake_popup");
    e1.innerHTML = '<h3> <strong> Drinking water intake </strong></h3>';
    e1.innerHTML += '<strong>COMID #: </strong>' + in_comid + '<br><strong>' + 'Source: </strong>' + in_sourceName;
    e1.innerHTML += '<br><strong>' + 'System: </strong>' + in_systemName;
    return e1;

}

//add the intakes to the map (only those in huc8s that were run)
function addIntakes() {
    intakes = L.geoJSON(intake_data, {
                style: {
                    weight: 0.0,
                    fill_weight : 0.0
                },
                filter: function(feature) {
                    huc_12 = feature.properties.HUC12;
                    huc_8 = huc_12.substring(0,8);
                    if(contains(hucsRun,huc_8)){
                        return true;
                    }
                    else {
                        return false;
                    }
                },
                onEachFeature: function onEachFeature(feature, layer) {
                    points = layer.getLatLngs();
                    //var center = points[Math.floor(points.length/2)];
                    var center = points[0];
                    if(typeof(center) != undefined ) {
                        var marker = L.marker(center);
                        marker.bindPopup(intakeContent(feature));
                        intakeMarkers.addLayer(marker);
                    }
                }
            }).addTo(map);
    intakeMarkers.addTo(map);
}


//add a legend for the huc coloring
function addHucLegend(){
    legend = L.control({position: 'bottomright'});
    legend.onAdd = function (map) {

        var div = L.DomUtil.create('div', 'info legend'),
            grades = [0, .1, .2, .3, .4, .5],
            labels = [];

        // loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++) {
            div.innerHTML +=
                '<i style="background:' + exceedanceColor(grades[i] + .01) + '"></i> ' +
                grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        }

        return div;
    };

    legend.addTo(map);
}
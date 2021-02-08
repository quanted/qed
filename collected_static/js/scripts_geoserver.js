var map;
var tiled;
var pureCoverage = false;
// pink tile avoidance
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 5;
// make OL compute scale according to WMS spec
OpenLayers.DOTS_PER_INCH = 25.4 / 0.28;

window.onload = init;

function init(){
    // if this is just a coverage or a group of them, disable a few items,
    // and default to jpeg format
    format = 'image/png';
    if(pureCoverage) {
        document.getElementById('filterType').disabled = true;
        document.getElementById('filter').disabled = true;
        document.getElementById('antialiasSelector').disabled = true;
        document.getElementById('updateFilterButton').disabled = true;
        document.getElementById('resetFilterButton').disabled = true;
        document.getElementById('jpeg').selected = true;
        format = "image/jpeg";
    }

    var bounds = new OpenLayers.Bounds(
        -9943448, 4201431.5,
        -8658679, 5233714.5
    );
    var options = {
        controls: [],
        maxExtent: bounds,
        maxResolution: 5018.62890625,
        projection: "EPSG:3857",
        units: 'm',
        numZoomLevels: 15
    };
    map = new OpenLayers.Map('map', options);
    
    setWidth(800);
    setHeight(600);

    // setup tiled layer
    tiled = new OpenLayers.Layer.WMS(
        "cite:huc12s05 - Tiled", "http://134.67.114.4/geoserver/cite/wms",
        {
            "LAYERS": 'cite:huc12s05',
            "STYLES": '',
            format: format,
            // minZoomLevel: 1,
            // maxZoomLevel: 5,
            transparent: true
        },
        {
            buffer: 0,
            displayOutsideMaxExtent: true,
            isBaseLayer: false,
            yx : {'EPSG:3857' : false}
        } 
    );
    tiled.setOpacity(0.3);

    var gmap = new OpenLayers.Layer.Google("Google Maps",
        { type: google.maps.MapTypeId.TERRAIN }
    );

    map.addLayers([gmap, tiled]);

    // build up all controls
    map.addControl(new OpenLayers.Control.PanZoomBar({
        position: new OpenLayers.Pixel(2, 2)
    }));
    map.addControl(new OpenLayers.Control.Navigation());
    map.zoomToExtent(bounds);
}

function setHTMLLoading(response){
    //document.getElementById('nodelist').innerHTML = response.responseText;
    document.getElementById('nodelist').innerHTML = "<em>SAM is still running...please wait...</em>";
    console.log(response.responseText);
}

// sets the HTML provided into the nodelist element
function setHTML(response){
    // Pure JS AJAX call
    if (window.XMLHttpRequest) { // Mozilla, Safari, ...
      httpRequest = new XMLHttpRequest();
    } else if (window.ActiveXObject) { // IE
      try {
        httpRequest = new ActiveXObject("Msxml2.XMLHTTP");
      } 
      catch (e) {
        try {
          httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
        } 
        catch (e) {}
      }
    }

    if (!httpRequest) {
        alert('Failed to create an XMLHTTP instance');
        return false;
    }

    data = response.responseText;  // HUC clicked data from Geoserver
    jid = document.getElementById('jid').innerHTML; // SAM run 'jid'
    console.log(jid);
    console.log(data);

    httpRequest.onreadystatechange = showHUCData;  // Callback method
    httpRequest.open("POST", "/geoserver/query/" + jid, true);
    httpRequest.setRequestHeader('Content-Type', 'application/json');
    httpRequest.send(data);  // POST the JSON to server

}

function showHUCData() {
    if (httpRequest.readyState === 4) {
        if (httpRequest.status === 200) {
            // alert(httpRequest.responseText);
            document.getElementById('nodelist').innerHTML = httpRequest.responseText;
        } else {
            alert('There was a problem with the request.');
        }
    }
}

function setWidth(size){
    var mapDiv = document.getElementById('map');
    var wrapper = document.getElementById('wrapper');
    
    if (size == "auto") {
        // reset back to the default value
        mapDiv.style.width = null;
        wrapper.style.width = null;
    }
    else {
        mapDiv.style.width = size + "px";
        wrapper.style.width = size + "px";
    }
    // notify OL that we changed the size of the map div
    map.updateSize();
}

function setHeight(size){
    var mapDiv = document.getElementById('map');
    
    if (size == "auto") {
        // reset back to the default value
        mapDiv.style.height = null;
    }
    else {
        mapDiv.style.height = size + "px";
    }
    // notify OL that we changed the size of the map div
    map.updateSize();
}
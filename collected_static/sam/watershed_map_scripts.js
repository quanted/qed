
// initialize the map
var map = L.map('map',{
    loadingControl: true,
    preferCanvas: true
});

var start_point = [39.609280, -92.100678];
var start_zoom = 8;
map.setView(start_point, start_zoom);

// read model output
readOutputJSON(); //async ajax call
readSummaryHUC8JSON(); //async ajax call - also triggers HUC12s

// add out data
var info_box_title = null;
var info_box_id = null;
var outLayer = null;



// load a tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    subdomains: ['a', 'b', 'c']
}).addTo(map);


// -------------- BASE MAP code -------------- //

var layer = L.esri.basemapLayer('NationalGeographic').addTo(map);
//var currentHucLayer = huc_basemaps.HUC8;       // raster HUC
huc8Layer = L.geoJson(huc8s, {
    style: hucStyle//,
    //onEachFeature: onEachFeatureClick
}).addTo(map);
map.on('click', onMapClick);



// --------------- INFO WINDOW code -------------- //
info_box_title = "Stream Segment Info";
info_box_id = "ComID";
var info = L.control();

info.onAdd = function (map) {
    this._div = L.DomUtil.create('div', 'stream_info');
    this.update();
    return this._div;
};

info.update = function (props) {
    this._div.innerHTML = '<h5>' + info_box_title + '</h5>' +
        '<table id="stream_info_table" style="margin-bottom: 0px !important; background: none !important;"> ' +
        '<tr><td>Latitude:</td> <td id="latVal"></td></tr>' +
        '<tr><td>Longitude:</td><td id="lngVal"></td></tr>' +
        '<tr><td>' + info_box_id + '</td><td id="boxid"></td></tr>';
};

info.addTo(map);
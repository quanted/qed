/**
 * Created by KWOLFE on 11/14/2016.
 */

var layerStreamSeg = null;
var latitude = '';
var longitude = '';

function onMapClick(e) {
    getStreamSegShape(e.latlng.lat, e.latlng.lng)
}
map.on('click', onMapClick);


function getStreamSegShape(lat, lng)
{
    var url = "/streamsegment";
    var latLngData = { "latitude": lat.toString(), "longitude": lng.toString() };
    latitude = lat.toString();
    longitude = lng.toString();
    $('#latVal').html(latitude);
    $('#lngVal').html(longitude);

    var sLatLngData = JSON.stringify(latLngData);
    //alert(sLatLngData);
    $.ajax({
        type:"POST",
        url: url,
        dataType: "json",
        data: sLatLngData,
        success: function(data, status, jqXHR) {
            addStreamSegment(data);
            return data;
        },
        error: function(jqXHR, status) {
            return null;
        }

    })
}

function addStreamSegment(data)
{
    if (layerStreamSeg != null)
        map.removeLayer(layerStreamSeg);

    var segStyle = {
        "color": "#ff0000",
        "weight": 5,
        "opacity": 0.9
    };

    //var streamSegData = JSON.parse(data);
    layerStreamSeg = L.geoJSON(data, {
        style: segStyle
    }).addTo(map);
}

function getEcoRegion()
{
    var url = "/ecoregion";
    //var latLngData = { "latitude": lat.toString(), "longitude": lng.toString() };
    var latLngData = { "latitude": latitude, "longitude": longitude };
    lat = latitude;
    lng = longitude;
    //$('#latVal').html(latitude);
    //$('#lngVal').html(longitude);

    var sLatLngData = JSON.stringify(latLngData);
    //alert(sLatLngData);
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: sLatLngData,
        success: function (data, status, jqXHR) {
            $('#ecoRegionId').html(data['id']);
            $('#ecoRegionName').html(data['name']);
            return data;
        },
        error: function (jqXHR, status) {
            return null;
        }

    })
}

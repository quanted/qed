google.load('maps', '2');
// Load version 2 of the Maps API

function updateLatLonFields(lat, lon) {
	document.getElementById("lat").value = lat;
	document.getElementById("lon").value = lon;
}

function getOSMMapType() {
	// Usage: map.addMapType(getOSMMapType());
	var copyright = new GCopyrightCollection('<a href="http://www.openstreetmap.org/">OpenStreetMap</a>');
	copyright.addCopyright(new GCopyright(1, new GLatLngBounds(new GLatLng(-90, -180), new GLatLng(90, 180)), 0, ' '));
	var tileLayer = new GTileLayer(copyright, 1, 18, {
		tileUrlTemplate : 'http://tile.openstreetmap.org/{Z}/{X}/{Y}.png',
		isPng : false
	});
	var mapType = new GMapType([tileLayer], G_NORMAL_MAP.getProjection(), 'OSM');
	return mapType;
}

function showMap() {
	window.gmap = new google.maps.Map2(document.getElementById('gmap'));
	// Default view of the world
	gmap.addControl(new google.maps.LargeMapControl());
	gmap.addControl(new google.maps.MapTypeControl());
	gmap.addMapType(getOSMMapType());
	gmap.enableContinuousZoom();
	gmap.enableScrollWheelZoom();

	var timer = null;

	gmap.setCenter(new google.maps.LatLng(41.25, -101.5), 3);

	google.maps.Event.addListener(gmap, "move", function() {
		var center = gmap.getCenter();
		updateLatLonFields(center.lat(), center.lng());

		// Wait a second, then figure out the timezone
		if (timer) {
			clearTimeout(timer);
			timer = null;
		}
		timer = setTimeout(function() {
			var location = document.getElementById("lat").value + ',' + document.getElementById("lon").value;
			geocode(location);
		}, 1500);

	});

	google.maps.Event.addDomListener(document.getElementById('crosshair'), 'dblclick', function() {
		gmap.zoomIn();
	});

	// Set up Geocoder
	window.geocoder = new google.maps.ClientGeocoder();
}

function geocodeComplete(result) {
	if (result.Status.code != 200) {
		alert('Could not geocode "' + result.name + '"');
		return;
	}
	var place = result.Placemark[0];
	// Only use first result
	document.getElementById("address").value = "";
	document.getElementById("address").value = place.address;
}

function geocode(location) {
	geocoder.getLocations(location, geocodeComplete);
};

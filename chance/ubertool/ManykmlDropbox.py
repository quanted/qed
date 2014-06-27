# -*- coding: utf-8 -*-
"""
Created on Wed May 23 16:13:01 2012

@author: cholla02
"""

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
  	<title>Endangered Species Mapping</title>
  	<style type="text/css">
		#map { width:500px; height:500px;}
		body { font-family:"Trebuchet MS", verdana,arial,sans-serif; 
				font-size:80%;
				}
		ul { list-style-type:none;
		}
		ul li a { margin-left:30px;}
		#view-gm { background-image:url(google.gif); background-repeat:no-repeat;
		}
		#download-kml {background-image:url(kml.png); background-repeat:no-repeat;
		}
		#map div { font-weight:bold;}
		#map #iwsw p { font-weight:normal !important;}
	</style>
    <script src="http://maps.google.com/maps?file=api&amp;v=3&amp;key='INSERT_Google_Maps_API_Key_Here'" type="text/javascript"></script>
	<script type="text/javascript">
		function showMap() {
			var geocoder = new GClientGeocoder();
			geocoder.setCache=null;
			// Google Maps caches KML files -- use a random query string parameter set to Date.
			var url_end = "?nocache=" + (new Date()).valueOf();
			var server_root = "http://www.littled.net/exp/";			
                        var kmlFile = "http://dl.dropbox.com/u/34957516/clarke.kmz";
                        var kmlFile2 = "http://dl.dropbox.com/u/34957516/raster.kmz";
                        var kmlFile3 = "http://dl.dropbox.com/u/34957516/T_sirtalis.kmz";
                        var kmlFile4 = "http://dl.dropbox.com/u/34957516/G_sila.kmz";

			var map = new GMap2(document.getElementById("map"));
			// Add controls
			map.addControl(new GLargeMapControl());
			map.addControl(new GMapTypeControl());
			geoxml = new GGeoXml(kmlFile);
                        geoxml2 = new GGeoXml(kmlFile2);
                        geoxml3 = new GGeoXml(kmlFile3);
                        geoxml4 = new GGeoXml(kmlFile4);
                        map.addOverlay(geoxml); 
                        map.addOverlay(geoxml2);
                        map.addOverlay(geoxml3); 
                        map.addOverlay(geoxml4);
			
			// Default zoom level
			var zl = 5;
			map.setCenter(new GLatLng(33.7489,-84.3881),zl);
		}
		window.onload = showMap;
	</script>
  </head>
  <body>
	<ul>
		<li id="view-gm"><a href="http://maps.google.co.uk/maps?f=q&amp;hl=en&amp;q=http%3A%2F%2Fwww.littled.net%2Fexp%2Fgmap.kml&amp;ie=UTF8&amp;ll=51.4832,-0.007896&amp;spn=0.004931,0.014591&amp;z=16&amp;om=1">View in Google Maps</a></li>
		<li id="download-kml"><a href="gmap.kml">Download KML file</a></li>
	</ul>
  	<div id="map"></div>
   </body>
</html>

/**
 * Created by KWOLFE on 10/13/2016.
 */
var streamNetwork = {
    streamNetwork: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
        layers: 4,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    })

};
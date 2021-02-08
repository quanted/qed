var huc_basemaps = {
    HUC2: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 0,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }),
    /*HUC4: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 1,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }),
    HUC6: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 2,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }),*/
    HUC8: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 3,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    })/*,
    HUC10: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 4,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }),
    HUC12: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/WBD_NP21_Simplified/MapServer/WmsServer?', {
        layers: 5,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    }),
    streamNetwork: L.tileLayer.wms('https://watersgeo.epa.gov/arcgis/services/NHDPlus_NP21/NHDSnapshot_NP21/MapServer/WmsServer??', {
        layers: 4,
        format: 'image/png',
        minZoom: 0,
        maxZoom: 18,
        transparent: true
    })*/
};
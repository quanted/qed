// Long polling for SAM results
$( document ).ready(function() {

    $('.sam_map').show();

    // Warn user not to refresh page
    alert('SAM run successfully submitted.  Do NOT refresh page.  ' +
        'This will result in duplicate model submissions and will slow down returning of model results.');

    var jid_ajax = document.getElementById('jid').innerHTML; // SAM run 'jid'
    //var timer = null;

    function updateTimer() {

        $.ajax({ 
            url: "/geoserver/sam_done/" + jid_ajax,
            method: 'POST',
            dataType: "json",
            success: function(data) {

                if (data.done) {
                    showMap(data.input, data.jid);
                    $('.sam_link').show();
                    $('#nodelist').html("<em>SAM has finished processing the spatial data.  Select HUC to view data.</em>");
                    alert('SAM is finished processing.  Results are now available to download and view on the map.');
                } else {
                    setTimeout(updateTimer, 10000); // poll again in 10s until: data == 'done'
                }

            },
            error: function( jqXHR, textStatus, errorThrown ){
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);

                setTimeout(updateTimer, 10000); // poll again in 10s
            }

        });

    }

    function showMap(input, jid) {

        var output_type = input.output_type;
        var output_time_avg_option = input.output_time_avg_option;
        var output_time_avg_conc = input.output_time_avg_conc;
        var output_tox_thres_exceed = input.output_tox_thres_exceed;
        var sqlViewStyle, sqlViewQuery, arg, colorRange, graphFileName;

        if (output_type == '1') {
            console.log('Not Mapping Daily Conc. Yet...');
            sqlViewStyle = "samMthStyle";
        } else {
            if (output_time_avg_option == '1') {
                switch (output_time_avg_conc) {
                    case '1':
                        console.log('Not Mapping Daily Conc. Yet...');
                        sqlViewStyle = "samMthStyle";
                        sqlViewQuery = "samMthAll";
                        arg = "mth:jun";
                        colorRange = 'r1:2;r2:4;r3:6;r4:8;r5:10';
                        break;
                    case '2':
                        sqlViewStyle = "samAnnStyle";
                        sqlViewQuery = "samAnnAll";
                        arg = "yr:29";
                        colorRange = 'r1:2;r2:4;r3:6;r4:8;r5:10';
                        break;
                }
            }
            else {
                switch (output_tox_thres_exceed) {
                    case '1':
                        sqlViewStyle = "samAnnStyle";
                        sqlViewQuery = "samAnnAll";
                        arg = "yr:29";
                        colorRange = 'r1:0.1;r2:0.2;r3:0.3;r4:0.4;r5:0.5';
                        //graphFileName =
                        break;
                    case '2':
                        sqlViewStyle = "samMthStyle";
                        sqlViewQuery = "samMthAll";
                        arg = "mth:jun";
                        colorRange = 'r1:0.1;r2:0.2;r3:0.3;r4:0.4;r5:0.5';
                        //graphFileName =
                        break;
                    case '3':
                        sqlViewStyle = "samAnnStyle";
                        sqlViewQuery = "samAnnAll";
                        arg = "yr:29";
                        colorRange = 'r1:2;r2:4;r3:6;r4:8;r5:10';
                        //graphFileName =
                        break;
                    case '4':
                        sqlViewStyle = "samMthStyle";
                        sqlViewQuery = "samMthAll";
                        arg = "mth:jun";
                        colorRange = 'r1:2;r2:4;r3:6;r4:8;r5:10';
                        //graphFileName = jid + "_month_streak_boxplot.png";
                        break;
                }
            }
        }

        //$('#sam_graph_1').attr( { 'src': graphFileName } );
        var colorRangeArray = colorRange.split(';');
        for (i=0;i<colorRangeArray.length;i++) {
            range = colorRangeArray[i].split(':');
            $('#legend_scale_' + (i + 1)).text(range[1]);
        }

        sam_output_layer = new OpenLayers.Layer.WMS(
            "SAM SQL View",
            "http://134.67.114.4/geoserver/cite/wms",
            {
                "LAYERS": 'cite:' + sqlViewStyle,
                "STYLES": 'samStyle',
                "format": format,
                "viewparams": 'jid:' + jid_ajax,
                "env": colorRange,
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
        sam_output_layer.setOpacity(0.3);

        map.removeLayer(tiled);
        map.addLayers([sam_output_layer]);
        console.log("Tried to switch baselayer");

        // support GetFeatureInfo
        map.events.register('click', map, function (e) {

            var params = {
                SERVICE: "WMS",
                REQUEST: "GetFeatureInfo",
                "Layers": 'cite:' + sqlViewQuery,
                styles: null,
                srs: map.layers[1].params.SRS,
                BBOX: map.getExtent().toBBOX(),
                WIDTH: map.size.w,
                HEIGHT: map.size.h,
                QUERY_LAYERS: 'cite:' + sqlViewQuery,
                INFO_FORMAT: 'application/json',  // 'application/vnd.ogc.gml', // If set to 'text/html', returned HTML is formatted using templates on Geoserver
                FEATURE_COUNT: 1,
                EXCEPTIONS: 'application/json' // "application/vnd.ogc.se_xml"
            };

            // handle the wms 1.3 vs wms 1.1 madness
            if(map.layers[1].params.VERSION == "1.3.0") {
                params.version = "1.3.0";
                params.j = parseInt(e.xy.x);
                params.i = parseInt(e.xy.y);
            } else {
                params.version = "1.1.1";
                params.x = parseInt(e.xy.x);
                params.y = parseInt(e.xy.y);
            }

            // merge filters
            if(map.layers[1].params.CQL_FILTER != null) {
                params.cql_filter = map.layers[1].params.CQL_FILTER;
            }
            if(map.layers[1].params.FILTER != null) {
                params.filter = map.layers[1].params.FILTER;
            }
            if(map.layers[1].params.FEATUREID) {
                params.featureid = map.layers[1].params.FEATUREID;
            }
            //                                                                 caller onComplete onFailure
            //OpenLayers.loadURL("http://134.67.114.4/geoserver/cite/wms", params, this, setHTML, setHTML);

            OpenLayers.Request.GET({
                url: "http://134.67.114.4/geoserver/cite/wms",
                params: params,
                callback: setHTML
            });

            OpenLayers.Event.stop(e);
        });
    }

    updateTimer(); //initiate the timer
});

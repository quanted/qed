// var baseUrl = "/hms/rest/api/hydrology/soilmoisture/";
var baseUrl = "/hms/rest/api/v3/hydrology/soilmoisture/";


$(function () {
    // form events
    $('#id_source').change(updateForm);
    document.getElementById("id_layers").options[0].selected = "selected";

    // $('#overview_block').accordion({
    //     collapsible: true,
    //     heightStyle: "content"
    // });
    $('#id_area_of_interest').on('change', updateAoISelection);

    setTimeout(setOverviewTabindex, 100);
    setTimeout(updateAoISelection, 100);

});

function setOutputUI() {
    setMetadata();
    setDataGraph2();
    return false;
}

function getParameters() {
    // Dataset specific request object
    var requestJson = {
        "source": $('#id_source').val(),
        "dateTimeSpan": {
            "startDate": $("#id_startDate").val(),
            "endDate": $('#id_endDate').val()
        },
        "geometry": {
            "point": {
                "latitude": $("#id_latitude").val(),
                "longitude": $("#id_longitude").val()
            },
            "geometryMetadata": {
                "stationID": $("#id_stationID").val()
            }
        },
        "dataValueFormat": $("#id_outputformat").val(),
        "temporalResolution": $("#id_temporalresolution").val(),
        "timeLocalized": $("#id_timelocalized").val(),
        "units": "default",
        "outputFormat": "json",
        "layers": $("#id_layers").val()
    };
    if($('#id_area_of_interest').val() === "Catchment Centroid"){
        delete requestJson["geometry"]["point"];
        requestJson["geometry"]["comid"] = $("#id_catchment_comid").val()
    }
    return requestJson;
}

function updateForm() {
    $('#id_source').change(function () {
        // if (document.input_table.layers) {
        var element = document.getElementById("id_source");
        var layers = document.getElementById("id_layers");
        if (element.options[element.selectedIndex].value === 'nldas') {
            layers.options.length = 0;
            layers.options[0] = new Option("0-10cm", "0-10");
            layers.options[1] = new Option("10-40cm", "10-40");
            layers.options[2] = new Option("40-100cm", "40-100");
            layers.options[3] = new Option("100-200cm", "100-200");
            layers.options[4] = new Option("0-100cm", "0-100");
            layers.options[5] = new Option("0-200cm", "0-200");
        }
        else if (element.options[element.selectedIndex].value === 'gldas') {
            layers.options.length = 0;
            layers.options[0] = new Option("0-10cm", "0-10");
            layers.options[1] = new Option("10-40cm", "10-40");
            layers.options[2] = new Option("40-100cm", "40-100");
        }
        document.getElementById("id_layers").options[0].selected = "selected";
    });
}

function updateAoISelection(){
    var source = $("#id_source").val();
    if(source === "ncei"){
        $("#id_area_of_interest").parent().parent().hide();
        $("#id_latitude").parent().parent().hide();
        $("#id_longitude").parent().parent().hide();
        $("#id_catchment_comid").parent().parent().hide();
    }
    else {
        $("#id_area_of_interest").parent().parent().show();
        var aoi = $('#id_area_of_interest').val();
        if (aoi === "Latitude/Longitude") {
            $("#id_latitude").parent().parent().show();
            $("#id_longitude").parent().parent().show();
            $("#id_catchment_comid").parent().parent().hide();
        } else {
            $("#id_latitude").parent().parent().hide();
            $("#id_longitude").parent().parent().hide();
            $("#id_catchment_comid").parent().parent().show();
        }
    }
}

function setOverviewTabindex(){
    $('#ui-id-3').attr('tabindex', '0');
    $('#ui-id-5').attr('tabindex', '0');
    $('#ui-id-7').attr('tabindex', '0');
    $('#ui-id-9').attr('tabindex', '0');
}